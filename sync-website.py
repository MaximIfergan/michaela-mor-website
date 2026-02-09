#!/usr/bin/env python3
"""
Website Sync for Michaela Mor's Portfolio
==========================================
Syncs collections from Google Drive to the website.

Usage:
    python3 sync-website.py

Reads Works_Metadata.csv and image folders from the configured Google Drive path,
then generates collection pages and updates gallery.html.
"""

import csv
import os
import re
import shutil
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()

# Google Drive source path (synced locally)
GDRIVE_BASE = Path(
    "/Users/maxim/Library/CloudStorage/GoogleDrive-maxim758@gmail.com/"
    ".shortcut-targets-by-id/1mwltaBGHjoB1FPQPAU1bXaTKjr9i9ZmQ/"
    "צילומי תערוכות ועבודות/Website Works"
)

CSV_FILENAME = "Works_Metadata.csv"


def slugify(name):
    """Convert a collection name to a URL-safe slug."""
    slug = name.lower().strip()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug


def read_csv(csv_path):
    """Read the Works_Metadata.csv and group rows by Collection."""
    collections = {}

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            collection_name = row.get('Collection', '').strip()
            if not collection_name:
                continue

            if collection_name not in collections:
                collections[collection_name] = {
                    'name': collection_name,
                    'slug': slugify(collection_name),
                    'works': [],
                    'year': '',
                }

            work = {
                'filename': row.get('Image filename', '').strip(),
                'title': row.get('Artwork title', '').strip(),
                'year_created': row.get('Year created', '').strip(),
                'year_presented': row.get('Year Presented', '').strip(),
                'medium': row.get('Medium', '').strip(),
                'dimensions': row.get('Dimensions', '').strip(),
                'exhibitions': row.get('Exhibitions', '').strip(),
            }

            collections[collection_name]['works'].append(work)

            # Use the most recent year presented as the collection year
            if work['year_presented']:
                current = collections[collection_name]['year']
                if not current or work['year_presented'] > current:
                    collections[collection_name]['year'] = work['year_presented']

    # Sort works by filename within each collection
    for col in collections.values():
        col['works'].sort(key=lambda w: w['filename'])

    return collections


def find_image(collection_folder, filename):
    """Find an image file in the collection folder, with fallback matching."""
    if not collection_folder.exists():
        return None

    # Exact match
    exact = collection_folder / filename
    if exact.exists():
        return exact

    # Case-insensitive match
    for f in collection_folder.iterdir():
        if f.name.lower() == filename.lower():
            return f

    return None


def copy_images(collection_name, works, dest_folder):
    """Copy images from Google Drive to the website images folder."""
    source_folder = GDRIVE_BASE / collection_name
    dest_path = Path(dest_folder)
    dest_path.mkdir(parents=True, exist_ok=True)

    copied = 0
    warnings = []

    for work in works:
        filename = work['filename']
        if not filename:
            continue

        source_file = find_image(source_folder, filename)
        if source_file:
            dest_file = dest_path / source_file.name
            # Update work filename to match actual file on disk
            work['filename'] = source_file.name
            if not dest_file.exists() or source_file.stat().st_mtime > dest_file.stat().st_mtime:
                shutil.copy2(source_file, dest_file)
                copied += 1
        else:
            warnings.append(f"  WARNING: Image not found: '{filename}' in '{collection_name}/'")

    return copied, warnings


def compress_images(folder_path):
    """Compress images using ImageMagick if available."""
    try:
        subprocess.run(['magick', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  ImageMagick not installed, skipping compression")
        return

    for img_path in Path(folder_path).glob('*'):
        if img_path.suffix.lower() in ('.jpg', '.jpeg', '.png'):
            try:
                subprocess.run([
                    'magick', str(img_path),
                    '-resize', '1920x1920>',
                    '-quality', '85',
                    '-gravity', 'southeast',
                    '-pointsize', '18',
                    '-fill', 'rgba(255,255,255,0.12)',
                    '-annotate', '+15+15', '\u00a9 Michaela Mor',
                    str(img_path)
                ], capture_output=True, check=True)
            except subprocess.CalledProcessError:
                print(f"  Warning: Could not process {img_path.name}")

    print("  Images compressed & watermarked")


def generate_collection_html(collection):
    """Generate the HTML page for a collection."""
    name = collection['name']
    image_path = f"images/Gallery/{name}"

    gallery_items = []
    for work in collection['works']:
        if not work['filename']:
            continue

        medium_info = work['medium']
        if work['dimensions']:
            medium_info += f", {work['dimensions']}" if medium_info else work['dimensions']

        year_display = work['year_created'] or work['year_presented'] or ''

        item = (
            f'                <div class="gallery-item" '
            f'data-title="{work["title"]}" '
            f'data-year="{year_display}" '
            f'data-medium="{medium_info}">\n'
            f'                    <img src="{image_path}/{work["filename"]}" '
            f'alt="{work["title"]}">\n'
            f'                    <div class="gallery-item-info">\n'
            f'                        <h3>{work["title"]}</h3>\n'
            f'                    </div>\n'
            f'                </div>'
        )
        gallery_items.append(item)

    gallery_items_html = '\n\n'.join(gallery_items)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Michaela Mor</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="nav">
        <div class="nav-container">
            <a href="index.html" class="nav-logo">Michaela Mor</a>
            <ul class="nav-menu">
                <li><a href="index.html">Home</a></li>
                <li><a href="gallery.html" class="active">Works</a></li>
                <li><a href="about.html">About</a></li>
                <li><a href="contact.html">Contact</a></li>
            </ul>
        </div>
    </nav>

    <!-- Collection Gallery -->
    <section class="gallery">
        <div class="container">
            <div class="gallery-grid">
{gallery_items_html}
            </div>

            <!-- Back to Works Link -->
            <div class="back-link">
                <a href="gallery.html">&larr; Back to Works</a>
            </div>
        </div>
    </section>

    <!-- Lightbox Modal -->
    <div id="lightbox" class="lightbox">
        <span class="lightbox-close">&times;</span>
        <img class="lightbox-content" id="lightbox-img">
        <div class="lightbox-caption">
            <h3 id="lightbox-title"></h3>
            <p id="lightbox-info"></p>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>
'''
    return html


def generate_gallery_html(collections_list):
    """Generate the gallery.html (Works page) with collection cards."""
    cards = []
    for col in collections_list:
        slug = col['slug']
        name = col['name']
        year = col['year']

        # Use first work's image as cover
        cover_image = ''
        for work in col['works']:
            if work['filename']:
                cover_image = f"images/Gallery/{name}/{work['filename']}"
                break

        if not cover_image:
            continue

        card = (
            f'                <a href="collection-{slug}.html" class="exhibition-folder">\n'
            f'                    <img src="{cover_image}" alt="{name}">\n'
            f'                    <div class="exhibition-info">\n'
            f'                        <h3>{name}</h3>\n'
            f'                        <p>{year}</p>\n'
            f'                    </div>\n'
            f'                </a>'
        )
        cards.append(card)

    cards_html = '\n\n'.join(cards)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Works - Michaela Mor</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="nav">
        <div class="nav-container">
            <a href="index.html" class="nav-logo">Michaela Mor</a>
            <ul class="nav-menu">
                <li><a href="index.html">Home</a></li>
                <li><a href="gallery.html" class="active">Works</a></li>
                <li><a href="about.html">About</a></li>
                <li><a href="contact.html">Contact</a></li>
            </ul>
        </div>
    </nav>

    <!-- Collections Grid -->
    <section class="exhibitions">
        <div class="container">
            <div class="exhibitions-grid">
{cards_html}
            </div>
        </div>
    </section>

    <script src="script.js"></script>
</body>
</html>
'''
    return html


def clean_old_collections(collections):
    """Remove old collection HTML files that are no longer in the CSV."""
    existing = list(SCRIPT_DIR.glob('collection-*.html'))
    valid_slugs = {c['slug'] for c in collections.values()}

    for f in existing:
        match = re.match(r'collection-(.+)\.html', f.name)
        if match and match.group(1) not in valid_slugs:
            f.unlink()
            print(f"  Removed stale: {f.name}")


def main():
    print("=" * 55)
    print("Michaela Mor - Website Sync")
    print("=" * 55)

    # Verify Google Drive path
    if not GDRIVE_BASE.exists():
        print(f"\nERROR: Google Drive folder not found:")
        print(f"  {GDRIVE_BASE}")
        print("\nMake sure Google Drive is synced and the path is correct.")
        return

    csv_path = GDRIVE_BASE / CSV_FILENAME
    if not csv_path.exists():
        print(f"\nERROR: {CSV_FILENAME} not found in Google Drive folder.")
        print("Export the Google Sheet as CSV and place it in the Website Works folder.")
        return

    # Read CSV
    print(f"\n[1/5] Reading {CSV_FILENAME}...")
    collections = read_csv(csv_path)
    print(f"  Found {len(collections)} collections:")
    for name, col in collections.items():
        print(f"    - {name} ({len(col['works'])} works, {col['year']})")

    # Copy images
    print(f"\n[2/5] Copying images from Google Drive...")
    all_warnings = []
    for name, col in collections.items():
        dest = SCRIPT_DIR / 'images' / 'Gallery' / name
        copied, warnings = copy_images(name, col['works'], dest)
        print(f"  {name}: {copied} new/updated images")
        all_warnings.extend(warnings)

    # Compress images
    print(f"\n[3/5] Compressing images...")
    for name in collections:
        dest = SCRIPT_DIR / 'images' / 'Gallery' / name
        if dest.exists():
            compress_images(dest)

    # Generate collection pages
    print(f"\n[4/5] Generating collection pages...")
    clean_old_collections(collections)
    for name, col in collections.items():
        html = generate_collection_html(col)
        output_file = SCRIPT_DIR / f"collection-{col['slug']}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  Created: {output_file.name}")

    # Generate gallery.html
    print(f"\n[5/5] Generating gallery.html...")
    # Sort by year descending (newest first)
    sorted_collections = sorted(
        collections.values(),
        key=lambda c: c['year'],
        reverse=True
    )
    gallery_html = generate_gallery_html(sorted_collections)
    with open(SCRIPT_DIR / 'gallery.html', 'w', encoding='utf-8') as f:
        f.write(gallery_html)
    print("  Updated: gallery.html")

    # Summary
    print(f"\n{'=' * 55}")
    if all_warnings:
        print("WARNINGS:")
        for w in all_warnings:
            print(w)
        print()

    total_works = sum(len(c['works']) for c in collections.values())
    print(f"SYNC COMPLETE - {len(collections)} collections, {total_works} works")
    print(f"{'=' * 55}")

    # Deploy to Cloudflare Pages
    print(f"\n[Deploy] Deploying to Cloudflare Pages...")
    try:
        result = subprocess.run(
            ['wrangler', 'pages', 'deploy', str(SCRIPT_DIR),
             '--project-name=michaela-mor-portfolio']
        )
        if result.returncode != 0:
            print("\n  Deploy failed. Make sure wrangler is installed and you're logged in:")
            print("    npm install -g wrangler")
            print("    wrangler login")
    except FileNotFoundError:
        print("  wrangler not found. Install it with: npm install -g wrangler")
        print("  Then log in with: wrangler login")


if __name__ == '__main__':
    main()
