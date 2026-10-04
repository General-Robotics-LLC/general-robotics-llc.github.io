"""Render the whole Wheeler robot as an engineering drawing.

Reads the triangle data written by export_wheeler.py, decides which parts to
draw, and renders an orthographic view on the graphics card. The drawing is
built from three flat renders of the same view:

    shade   each part's saved colour, lit from a fixed direction
    ident   a unique colour per part, so borders between parts can be found
    normal  the surface direction, so creases within a part can be found

Lines are drawn wherever the part or the surface direction changes, and the
shading is mapped onto one ink colour so the result suits the website.

Run with the generator's Python environment:

    PYOPENGL_PLATFORM=egl ~/gr-image-generator/.venv/bin/python render_wheeler.py --out wheeler.png

Which parts are drawn
---------------------
The CAD file was saved with covers and some other parts hidden so the inside
could be worked on. "Whole robot" here means: everything that was visible,
plus the hidden parts listed in SHOW_HIDDEN below. Hidden parts that are
superseded designs, reference copies, construction geometry or space
reservations stay hidden (see KEEP_HIDDEN).
"""
import argparse
import json
import re

import numpy as np

# Hidden parts to switch back on, matched against "group path / part label".
SHOW_HIDDEN = [
    r"lid / Individual components\d* / Lid( front (left|right))?( — |\d+ — )",   # the four top-cover quarters
    r"Electronics lid — rocker switch and power meter",                          # electronics cover
    r"lidar / Individual components\d* / S2 / ",                                  # lidar body
    r"head / Individual components\d* / COMPOUND",                                # head shell pieces
    r"right_antenna / Individual components\d* / COMPOUND",
    r"(left|right)_tyre / Individual components\d* / ",                           # tyre
    r"(left|right)_wheel / Individual components\d* / ",                          # wheel pieces
    r"base_link / Individual components / body ",                                 # base body piece
]
# Never drawn, even if a SHOW_HIDDEN pattern matches.
KEEP_HIDDEN = re.compile(
    r"SUPERSEDED|REJECTED|reference|fit prototype|construction|Previous|Unplaced|envelope|clearance|"
    r"Cover_Design|Cutouts|Blank|removed|reserved|not installed|uninstalled|Well_Removed|S2_Floor|"
    r"Original native|Upright lift|/ geometry\d*( /|$)", re.I)

INK = np.array([18, 39, 31]) / 255.0        # site ink colour (dark forest green)
PAPER = np.array([255, 253, 247]) / 255.0   # site plate colour


def choose_parts(records, extra_show=(), extra_hide=()):
    """Return (drawn, switched_on): the records to draw and those that were hidden in the file."""
    show = [re.compile(p) for p in list(SHOW_HIDDEN) + list(extra_show)]
    hide = [re.compile(p) for p in extra_hide]
    drawn, switched_on = [], []
    for r in records:
        if "error" in r or r["type"] == "Mesh::Feature" and r["label"].endswith(" visual"):
            continue
        text = " / ".join(r["path"]) + " / " + r["label"]
        if any(h.search(text) for h in hide):
            continue
        saved_visible = r["visible"] and all(r["path_visible"])
        if saved_visible:
            drawn.append(r)
        elif all(r["path_visible"]) and not KEEP_HIDDEN.search(text) and any(s.search(text) for s in show):
            drawn.append(r)
            switched_on.append(r)
    return drawn, switched_on


def look_at(direction, up=(0, 0, 1)):
    """Camera rotation whose -Z axis points along ``direction`` (camera looks that way)."""
    f = np.asarray(direction, float)
    f /= np.linalg.norm(f)
    s = np.cross(f, up)
    s /= np.linalg.norm(s)
    u = np.cross(s, f)
    return np.column_stack([s, u, -f])


def build_buffers(verts, faces, parts, light):
    """Expand the chosen parts into unshared triangles with three colour sets."""
    tri_ids = np.concatenate([np.arange(p["tri_start"], p["tri_start"] + p["tri_count"]) for p in parts])
    part_of = np.concatenate([np.full(p["tri_count"], i, np.int32) for i, p in enumerate(parts)])
    tris = verts[faces[tri_ids]]                                   # T x 3 x 3
    n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    length = np.linalg.norm(n, axis=1, keepdims=True)
    keep = length[:, 0] > 1e-9
    tris, n, part_of = tris[keep], n[keep] / length[keep], part_of[keep]
    base = np.array([p["colour"] or (0.7, 0.7, 0.7) for p in parts], np.float32)[part_of]
    # Two-sided diffuse light plus ambient; CAD faces are not always consistently wound.
    diffuse = np.abs(n @ light)
    shade = base * (0.42 + 0.58 * diffuse)[:, None]
    ident = np.stack([(part_of * 7919 + 13) % 251, (part_of * 104729 + 7) % 241, (part_of * 1299709 + 3) % 239], 1) / 255.0
    return tris.reshape(-1, 3).astype(np.float32), n, shade, ident.astype(np.float32)


def render_flat(positions, colours, cam_pose, half_w, half_h, size, depth_range):
    """Render unlit triangles with per-triangle colours; returns an H x W x 3 float image."""
    import pyrender
    rgba = np.concatenate([np.repeat(colours, 3, axis=0), np.ones((len(positions), 1), np.float32)], 1)
    prim = pyrender.Primitive(positions=positions, color_0=rgba, mode=4)
    scene = pyrender.Scene(bg_color=[1.0, 1.0, 1.0, 1.0], ambient_light=[1.0, 1.0, 1.0])
    scene.add(pyrender.Mesh([prim]))
    cam = pyrender.OrthographicCamera(xmag=half_w, ymag=half_h, znear=depth_range[0], zfar=depth_range[1])
    scene.add(cam, pose=cam_pose)
    renderer = pyrender.OffscreenRenderer(size[0], size[1])
    colour, _ = renderer.render(scene, flags=pyrender.RenderFlags.FLAT | pyrender.RenderFlags.SKIP_CULL_FACES)
    renderer.delete()
    return colour.astype(np.float32) / 255.0


def edges_from(image, threshold):
    """Mark pixels whose value differs from the pixel to the right or below."""
    d = np.zeros(image.shape[:2], bool)
    d[:, :-1] |= np.abs(image[:, 1:] - image[:, :-1]).max(2) > threshold
    d[:-1, :] |= np.abs(image[1:, :] - image[:-1, :]).max(2) > threshold
    return d


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--data", default="/home/kelsey-j-harvey/gr-image-generator/wheeler-render/wheeler_parts")
    ap.add_argument("--out", required=True)
    ap.add_argument("--view", type=float, nargs=3, default=[-1.0, 1.25, -0.62],
                    help="Direction the camera looks along, in the robot's coordinates.")
    ap.add_argument("--height", type=int, default=2400, help="Output height in pixels.")
    ap.add_argument("--saved-state", action="store_true", help="Draw only what was visible in the saved file.")
    ap.add_argument("--show", action="append", default=[], help="Extra pattern of hidden parts to draw.")
    ap.add_argument("--hide", action="append", default=[], help="Pattern of parts to leave out.")
    ap.add_argument("--colour", action="store_true", help="Keep the CAD colours instead of one ink.")
    args = ap.parse_args()

    data = np.load(args.data + ".npz")
    records = json.load(open(args.data + ".json"))
    if args.saved_state:
        SHOW_HIDDEN.clear()
    parts, switched_on = choose_parts(records, args.show, args.hide)
    print("parts drawn:", len(parts), "of which were hidden in the file:", len(switched_on))
    for r in switched_on:
        print("  ON:", " / ".join(r["path"][-2:]), "/", r["label"])

    rot = look_at(args.view)
    light = rot @ np.array([-0.45, 0.55, 0.70])
    light /= np.linalg.norm(light)
    positions, normals, shade, ident = build_buffers(data["vertices"], data["faces"], parts, light)
    print("triangles:", len(positions) // 3)

    # Frame the model: project onto the camera axes and pad the bounding box.
    cam_xy = positions @ rot[:, :2]
    lo, hi = cam_xy.min(0), cam_xy.max(0)
    centre_xy = (lo + hi) / 2
    half = (hi - lo) / 2 * 1.06
    depth = positions @ rot[:, 2]
    eye = rot[:, 0] * centre_xy[0] + rot[:, 1] * centre_xy[1] + rot[:, 2] * (depth.max() + 50)
    pose = np.eye(4)
    pose[:3, :3], pose[:3, 3] = rot, eye
    scale = 2                                     # render at twice the size, then reduce
    h = args.height * scale
    w = int(round(h * half[0] / half[1] / 2) * 2)
    rng = (1.0, float(depth.max() - depth.min() + 100))

    shaded = render_flat(positions, shade, pose, half[0], half[1], (w, h), rng)
    idmap = render_flat(positions, ident, pose, half[0], half[1], (w, h), rng)
    cam_normals = np.abs(normals @ rot) * 0.5 + 0.25      # view-space direction, sign-free
    normal = render_flat(positions, cam_normals.astype(np.float32), pose, half[0], half[1], (w, h), rng)

    outline = edges_from(idmap, 0.02)
    crease = edges_from(normal, 0.16) & ~outline
    background = (idmap > 0.995).all(2)

    if args.colour:
        img = shaded.copy()
    else:
        lum = shaded @ np.array([0.299, 0.587, 0.114])
        tone = np.clip((lum - 0.05) / 0.9, 0, 1) ** 0.85
        tone = 0.30 + 0.70 * tone                         # keep the darkest parts readable
        img = INK + (PAPER - INK) * tone[..., None]
    img[crease] = img[crease] * 0.55 + INK * 0.45
    img[outline] = INK
    img[background & ~outline] = PAPER

    from PIL import Image
    out = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).resize((w // scale, h // scale), Image.LANCZOS)
    out.save(args.out)
    print("saved", args.out, out.size)


if __name__ == "__main__":
    main()
