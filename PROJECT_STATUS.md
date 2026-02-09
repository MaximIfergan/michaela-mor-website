# Project Status - Michaela Mor Portfolio

**Last Updated:** February 9, 2026
**Live Site:** https://michaela-mor.com
**Hosting:** Cloudflare Pages (project: michaela-mor-portfolio)
**Domain Registrar:** Cloudflare
**Repository:** https://github.com/MaximIfergan/michaela-mor-portfolio (private)

---

## Current State: LIVE

The website is deployed on Cloudflare Pages with a custom domain.
Migrated from GitHub Pages to Cloudflare Pages for custom domain support + private repo.

---

## What's Working

- Home page with hero image (static, no scroll)
- Works page with collection-based gallery grid
- Collection pages with lightbox gallery (4 collections, 38 works)
- About page with CV
- Contact page with email + Instagram
- Fast page transitions (~180ms)
- Mobile responsive design
- Automated sync pipeline from Google Drive
- Auto-deploy to Cloudflare Pages via wrangler (integrated in sync-website.py)
- Custom domain: michaela-mor.com (SSL via Cloudflare)

---

## Recent Session (Feb 9, 2026)

### Completed

1. **Collection-Based Pipeline**
   - Replaced exhibition-based system with collection-based organization
   - Works grouped by Collection (not Exhibition) since some works appear in multiple exhibitions
   - Metadata managed via Google Sheet (exported as CSV)

2. **Google Drive Auto-Sync**
   - `sync-website.py` reads directly from shared Google Drive folder
   - Reads `Works_Metadata.csv` for metadata
   - Copies and compresses images automatically
   - Generates all collection HTML pages and gallery.html

3. **Current Collections**
   - OPEN STUDIO Recidensy (8 works, 2026)
   - Collection (4 works, 2024)
   - Ink (16 works, 2024)
   - Nostalgia for the Present Body (10 works, 2023)

4. **Watermark**
   - All images get a subtle "© Michaela Mor" watermark (12% opacity, bottom-right)
   - Applied automatically during the compression step via ImageMagick

5. **Cleanup**
   - Removed old exhibition-1 through exhibition-4 (placeholder content)
   - Removed old add-exhibition.py and EXHIBITION_TEMPLATE.md
   - Removed Bezalel Academy images

---

## Known Issues / TODO

1. **Desktop hero image** - User noted mobile changes affected desktop. May need adjustment.

---

## How to Continue

### Syncing & Deploying (one command)
```bash
# Michaela updates Google Sheet, exports CSV to Drive folder
# Then run:
python3 sync-website.py
# This syncs from Google Drive AND deploys to Cloudflare Pages automatically
```

### Backing up to Git (optional, recommended)
```bash
git add .
git commit -m "sync website"
git push
```
Git is no longer required for deployment, but recommended for version history and backup.

### Making CSS/HTML Changes
```bash
# Edit files, then deploy:
wrangler pages deploy . --project-name=michaela-mor-portfolio
# Or run sync-website.py which deploys at the end
```

### Michaela's Workflow
1. Add/edit works in the Google Sheet
2. Place images in the correct collection subfolder in Google Drive
3. Export sheet as CSV (`Works_Metadata.csv`) to the Website Works folder
4. Tell Maxim to run sync

### Google Drive Location
```
Google Drive > צילומי תערוכות ועבודות > Website Works
├── Works_Metadata.csv
├── Collection/
├── Ink/
├── Nostalgia for the Present Body/
└── OPEN STUDIO Recidensy/
```

### CSV Columns
`Collection, Exhibitions, Year Presented, Artwork title, Year created, Medium, Dimensions, Image filename`

### Deployment Stack
| Tool | Purpose |
|------|---------|
| Cloudflare Pages | Hosting (serves the website) |
| Cloudflare DNS | Domain management (michaela-mor.com) |
| Wrangler CLI | Deploys files from terminal to Cloudflare Pages |
| Node.js / npm | Runtime for wrangler (`brew install node`, `npm install -g wrangler`) |
| Git / GitHub | Version control & backup (private repo, not used for deployment) |

### First-Time Setup (new machine)
```bash
brew install node
npm install -g wrangler
wrangler login
```

---

## Key Files

| File | Purpose |
|------|---------|
| `index.html` | Home page |
| `gallery.html` | Works listing (auto-generated) |
| `collection-*.html` | Collection pages (auto-generated) |
| `about.html` | CV page |
| `contact.html` | Contact info |
| `style.css` | All styles |
| `script.js` | Transitions, lightbox |
| `sync-website.py` | Google Drive sync pipeline |

---

## Technical Reference

### Image Compression
Handled automatically by `sync-website.py` (max 1920px, 85% quality via ImageMagick)

### CSS Variables (style.css)
```css
--primary-color: #2c2c2c
--secondary-color: #8b9da8
--text-color: #4a4a4a
--border-color: #f0f0f0
--main-font: 'Sofia Sans', sans-serif
```

### Page Transitions
- Fade-out: 80ms (script.js line 20)
- Fade-in: 100ms (style.css line 62)

---

## Contact Info

- **Artist:** Michaela Mor
- **Email:** michaelasga1998@gmail.com
- **Instagram:** @michaellamor
- **Phone:** 054-3451679

---

*This file tracks project status for continuity between sessions.*
