# What the Phage v2.0 — Website

Modern landing page + interactive result explorer for the
[What the Phage](https://github.com/replikation/What_the_Phage) v2.0 platform
(branch `backbone_rework`).

- **`index.html`** — landing page: pipeline, tools, features, how-to-run, live demo, publication.
- **`viewer.html`** — interactive result explorer (7 tabs, sample switcher) loaded from bundled demo results.
- **`assets/`** — css, js, images, and demo result JSONs (`assets/data/`).

## Demo data

Bundled per-sample result JSONs from real WtP v2.0 runs:

| File | Sample |
| --- | --- |
| `assets/data/all_pos_phage_results.json` | synthetic positive control |
| `assets/data/ERR576943_raw_assembly_results.json` | clinical *E. coli* assembly |
| `assets/data/ERR576946_raw_assembly_results.json` | clinical *E. coli* assembly |

To refresh/add samples, copy a `*_results.json` from a WtP run
(`results/report/<sample>_results.json`) into `assets/data/` and register it in the
`DEMO_FILES` array at the top of the script in `viewer.html`.

## Local preview

```bash
# from this directory
python3 -m http.server 8000
# open http://localhost:8000
```

## Deploy to GitHub Pages

The site is fully static — no build step.

1. Create a new repository on GitHub (e.g. `WtP_v2.0_webpage`).
2. From this folder:

```bash
git init
git add .
git commit -m "WtP v2.0 website: landing + result explorer"
git branch -M main
git remote add origin https://github.com/<USER>/<REPO>.git
git push -u origin main
```

3. In the repo: **Settings → Pages → Source: Deploy from a branch → Branch `main` → folder `/ (root)`** → Save.
4. Your site will be live at `https://<USER>.github.io/<REPO>/` within a minute or two.

> Note: `viewer.html` loads the demo JSONs with `fetch()` — this requires serving over
> HTTP(S) (GitHub Pages qualifies). Opening `index.html` via `file://` will block the fetch.