# Source images

Originals that `tools/prepare_images.py` turns into the web-ready files in `assets/img/`.

| File | What it is |
| --- | --- |
| `wheeler-whole.png` | Engineering drawing of the whole Wheeler robot, rendered from the CAD model |
| `founder-portrait.jpg` | Founder portrait |

## How the Wheeler drawing is made

The drawing is rendered from a copy of the Wheeler CAD assembly, never from the working file. The assembly is normally saved with its covers hidden so the inside can be worked on; for this picture the top cover, electronics cover, lidar body, head shell, wheels and tyres are switched back on. Superseded designs, reference copies and construction geometry stay hidden.

The render is orthographic. Outlines are drawn where one part meets another and where a surface changes direction, and the shading is mapped onto the site's ink colour so the picture reads as a drawing.

The export and render scripts are kept with the robot's engineering files, not in this public repository.
