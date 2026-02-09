# Project Status - Michaela Mor Portfolio

**Last Updated:** February 9, 2026
**Live Site:** https://maximifergan.github.io/michaela-mor-portfolio/
**Repository:** https://github.com/MaximIfergan/michaela-mor-portfolio

---

## Current State: LIVE

The website is deployed and functional on GitHub Pages.

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

4. **Cleanup**
   - Removed old exhibition-1 through exhibition-4 (placeholder content)
   - Removed old add-exhibition.py and EXHIBITION_TEMPLATE.md
   - Removed Bezalel Academy images

---

## Known Issues / TODO

1. **Desktop hero image** - User noted mobile changes affected desktop. May need adjustment.

---

## How to Continue

### Syncing from Google Drive
```bash
# Michaela updates Google Sheet, exports CSV to Drive folder
# Then run:
python3 sync-website.py

# Push:
git add .
git commit -m "Sync collections from Google Drive"
git push
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

### Making CSS/HTML Changes
```bash
git add .
git commit -m "Description"
git push
# Live in ~1 minute
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

### Git Config
```bash
git config http.postBuffer 524288000  # 500MB buffer for large pushes
```

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
