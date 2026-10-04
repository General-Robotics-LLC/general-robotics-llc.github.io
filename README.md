# General Robotics website

The public website of General Robotics: one hand-written page in HTML, CSS and JavaScript. There is no build step and no framework. What is in this folder is what the browser receives.

Live address: https://generalroboticsllc.com/ (since 4 October 2026)
GitHub's address for the same site: https://general-robotics-llc.github.io/ (forwards to the live address)

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

### How the domain is connected

The domain `generalroboticsllc.com` is registered at GoDaddy and served by GitHub Pages. It was switched on 4 October 2026.

- This repository's `CNAME` file and its Pages settings name `generalroboticsllc.com` as the custom domain.
- GoDaddy's DNS records for the domain point at GitHub Pages:
  - four `A` records for `@`: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
  - a `CNAME` record for `www` pointing to `general-robotics-llc.github.io` (GitHub forwards `www` to the bare domain)
- The mail records (`MX`, `TXT`, `autodiscover`, `email`) belong to the Microsoft 365 email plan. Do not change them, or mail stops working.

GitHub's current instructions, in case the addresses ever change: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site

### Still to do after launch

1. Tick "Enforce HTTPS" in the repository's Pages settings once GitHub has issued the certificate (up to 24 hours after the switch).
2. Send a test message to `contact@generalroboticsllc.com` and confirm it arrives.
3. Decide what to do with the old GoDaddy Websites + Marketing site. It is no longer connected to the domain, and was not cancelled.
