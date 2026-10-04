# General Robotics website

The public website of General Robotics: one hand-written page in HTML, CSS and JavaScript. There is no build step and no framework. What is in this folder is what the browser receives.

Live address (after launch): https://generalroboticsllc.com/
Preview address: https://general-robotics-llc.github.io/

## Files

| Path | What it is |
| --- | --- |
| `index.html` | The page. Sections in order: hero, purpose, standard (the motto), craft, today, contact |
| `404.html` | Shown for addresses that do not exist |
| `assets/css/site.css` | All styling. Colours, type sizes and spacing are named values at the top |
| `assets/js/site.js` | Small conveniences (menu, scroll reveals). The page works without it |
| `assets/img/` | Web-ready images, the emblem in four colourways, the share card |
| `assets/fonts/` | Fraunces and Source Serif 4, self-hosted, with their licences |
| `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png`, `icon-192.png` | Browser and home-screen icons |
| `site.webmanifest`, `robots.txt`, `sitemap.xml` | Information for browsers and search engines |
| `tools/prepare_images.py` | Regenerates the images in `assets/img/` from the brand folder |
| `_source/` | Original files for the Wheeler drawing and the founder portrait |
| `NOTICE.md` | Rights and third-party licences |

## Viewing it on your computer

From this folder:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000/ in a browser.

## Making changes

**Words.** Edit `index.html`. Each section is marked with a comment banner.

**Colours and type.** Edit the block headed "Design tokens" at the top of `assets/css/site.css`. Every colour on the page comes from there.

**Emblem colour.** The emblem colour is still being decided. The page uses option B (green, cream and gold). To see another option without changing anything, add `?emblem=a`, `b`, `c` or `d` to the address. To change the default, replace `emblem-b.svg` with the chosen letter in `index.html` and `404.html`, copy that file over `favicon.svg`, and regenerate the PNG icons.

**Pictures.** Replace the source artwork in the brand folder, then run:

```bash
python3 tools/prepare_images.py "/path/to/GR Branding/"
```

It needs Python 3 with Pillow and NumPy. It crops the painted picture out of each advertisement (the page sets its own lettering as real text), and writes WebP and JPEG copies at several widths.

**Founder portrait.** Replace `_source/founder-portrait.jpg` and run the script above.

## How it is built

- **No dependencies.** No libraries, analytics, cookies or third-party requests. Fonts are served from this site.
- **Works without JavaScript.** The script only adds the mobile menu toggle, a header hairline, scroll reveals and the emblem preview.
- **Responsive.** Layout changes at 60rem and 46rem. Images are offered at several widths so phones download smaller files.
- **Accessible.** Semantic landmarks, a skip link, visible focus rings, alternative text on every picture, and text contrast of at least 4.5 to 1. Motion is switched off for people who ask their device to reduce it.
- **Honest.** Concept paintings are captioned as concept artwork. The Wheeler drawing is captioned as a development model.

## Publishing

The site is served by GitHub Pages from the `main` branch of this repository. Pushing to `main` publishes within a minute or two.

### Launch checklist (moving generalroboticsllc.com here)

1. In the repository's Pages settings, set the custom domain to `generalroboticsllc.com`. This adds a `CNAME` file.
2. At GoDaddy, in the domain's DNS records, point the domain at GitHub Pages:
   - four `A` records for `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - a `CNAME` record for `www` pointing to `general-robotics-llc.github.io`
   - leave the mail (`MX`) and verification (`TXT`) records as they are
3. Wait for GitHub to issue the certificate, then tick "Enforce HTTPS".
4. Check that `contact@generalroboticsllc.com` receives mail before the page is announced.
5. Turn off or cancel the old GoDaddy website builder site once the new one is confirmed live.

Check GitHub's current instructions before step 2, in case the addresses have changed: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site
