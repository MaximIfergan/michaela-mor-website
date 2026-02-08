#!/usr/bin/env python3
"""
Exhibition Generator for Michaela Mor's Website
================================================
This script processes an exhibition folder and generates the HTML page.

Usage:
    python3 add-exhibition.py <exhibition_folder>

The exhibition folder should contain:
    - Images (jpg, jpeg, png)
    - exhibition_data.txt (filled template)

The script will:
1. Copy images to images/Gallery/[Exhibition Name]/
2. Compress images using compress-images.sh
3. Create a new exhibition-X.html page
4. Add the exhibition to gallery.html
"""

import sys
import os
import re
import shutil
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()


def parse_exhibition_file(filepath):
    """Parse the exhibition data file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    data = {
        'name': '',
        'year': '',
        'location': '',
        'artworks': []
    }

    # Extract exhibition info
    name_match = re.search(r'Exhibition Name:\s*(.+)', content)
    year_match = re.search(r'Year:\s*(\d+)', content)
    location_match = re.search(r'Location.*?:\s*(.+)', content)

    if name_match:
        data['name'] = name_match.group(1).strip()
    if year_match:
        data['year'] = year_match.group(1).strip()
    if location_match:
        data['location'] = location_match.group(1).strip()

    # Extract artworks
    artwork_blocks = re.split(r'\n---\n', content)

    for block in artwork_blocks:
        if 'Image filename:' in block:
            artwork = {}

            filename_match = re.search(r'Image filename:\s*(.+)', block)
            title_match = re.search(r'Artwork title:\s*(.+)', block)
            art_year_match = re.search(r'Year created:\s*(.+)', block)
            medium_match = re.search(r'Medium.*?:\s*(.+)', block)
            dimensions_match = re.search(r'Dimensions.*?:\s*(.+)', block)

            if filename_match:
                artwork['filename'] = filename_match.group(1).strip()
            if title_match:
                artwork['title'] = title_match.group(1).strip()
            else:
                artwork['title'] = 'Untitled'
            if art_year_match:
                artwork['year'] = art_year_match.group(1).strip()
            else:
                artwork['year'] = data['year']
            if medium_match:
                artwork['medium'] = medium_match.group(1).strip()
            else:
                artwork['medium'] = ''
            if dimensions_match:
                artwork['dimensions'] = dimensions_match.group(1).strip()
            else:
                artwork['dimensions'] = ''

            if artwork.get('filename'):
                data['artworks'].append(artwork)

    return data


def find_data_file(folder_path):
    """Find the exhibition data file in the folder."""
    folder = Path(folder_path)

    # Look for common names
    possible_names = [
        'exhibition_data.txt', 'data.txt', 'info.txt',
        'exhibition.txt', 'metadata.txt', 'details.txt'
    ]

    for name in possible_names:
        data_file = folder / name
        if data_file.exists():
            return data_file

    # Look for any .txt file
    txt_files = list(folder.glob('*.txt'))
    if txt_files:
        return txt_files[0]

    return None


def find_images(folder_path):
    """Find all images in the folder."""
    folder = Path(folder_path)
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
    images = []
    for ext in extensions:
        images.extend(folder.glob(ext))
    return sorted(images)


def copy_images(source_folder, dest_folder, images):
    """Copy images to the destination folder."""
    dest_path = Path(dest_folder)
    dest_path.mkdir(parents=True, exist_ok=True)

    copied = []
    for img in images:
        dest_file = dest_path / img.name
        shutil.copy2(img, dest_file)
        copied.append(img.name)
        print(f"  Copied: {img.name}")

    return copied


def compress_images(folder_path):
    """Run the compress-images.sh script on the folder."""
    compress_script = SCRIPT_DIR / 'images' / 'compress-images.sh'

    if not compress_script.exists():
        # Try alternative location
        compress_script = SCRIPT_DIR / 'compress-images.sh'

    if not compress_script.exists():
        print("  Warning: compress-images.sh not found, skipping compression")
        return False

    # Check if ImageMagick is installed
    try:
        subprocess.run(['magick', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  Warning: ImageMagick not installed, skipping compression")
        print("  Install with: brew install imagemagick")
        return False

    try:
        result = subprocess.run(
            ['bash', str(compress_script), str(folder_path)],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("  Images compressed successfully!")
            return True
        else:
            print(f"  Warning: Compression returned non-zero: {result.stderr}")
            return False
    except Exception as e:
        print(f"  Warning: Could not compress images: {e}")
        return False


def get_next_exhibition_number():
    """Find the next available exhibition number."""
    existing = list(SCRIPT_DIR.glob('exhibition-*.html'))
    if not existing:
        return 1
    numbers = []
    for f in existing:
        match = re.search(r'exhibition-(\d+)\.html', f.name)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers) + 1 if numbers else 1


def generate_exhibition_html(data, exhibition_num):
    """Generate the exhibition HTML page."""
    image_path = f"images/Gallery/{data['name']}"

    # Generate gallery items
    gallery_items = []
    for i, artwork in enumerate(data['artworks'], 1):
        medium_info = artwork['medium']
        if artwork['dimensions']:
            medium_info += f", {artwork['dimensions']}" if medium_info else artwork['dimensions']

        item = f'''                <div class="gallery-item" data-title="{artwork['title']}" data-year="{artwork['year']}" data-medium="{medium_info}">
                    <img src="{image_path}/{artwork['filename']}" alt="{artwork['title']}">
                    <div class="gallery-item-info">
                        <h3>{artwork['title']}</h3>
                    </div>
                </div>'''
        gallery_items.append(item)

    gallery_items_html = '\n\n'.join(gallery_items)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['name']} - Michaela Mor</title>
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


    <!-- Exhibition Gallery -->
    <section class="gallery">
        <div class="container">
            <div class="gallery-grid">
                <!-- {data['name']} {data['year']} -->
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


def update_gallery_html(data, exhibition_num):
    """Add the new exhibition to gallery.html."""
    gallery_file = SCRIPT_DIR / 'gallery.html'

    with open(gallery_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the first image to use as cover
    if data['artworks']:
        cover_image = f"images/Gallery/{data['name']}/{data['artworks'][0]['filename']}"
    else:
        cover_image = "images/placeholder.jpg"

    # Create new exhibition entry
    new_entry = f'''
                <a href="exhibition-{exhibition_num}.html" class="exhibition-folder">
                    <img src="{cover_image}" alt="{data['name']}">
                    <div class="exhibition-info">
                        <h3>{data['name']}</h3>
                        <p>{data['year']}</p>
                    </div>
                </a>'''

    # Insert after the opening of exhibitions-grid
    insert_marker = '<div class="exhibitions-grid">'
    insert_pos = content.find(insert_marker)

    if insert_pos != -1:
        insert_pos += len(insert_marker)
        next_newline = content.find('\n', insert_pos)
        if next_newline != -1:
            content = content[:next_newline] + new_entry + content[next_newline:]

    with open(gallery_file, 'w', encoding='utf-8') as f:
        f.write(content)


def auto_generate_data(images, folder_name):
    """Auto-generate exhibition data when no data file exists."""
    # Extract exhibition name and year from folder name
    # Expected format: "Exhibition Name 2025" or "Exhibition Name"
    year_match = re.search(r'(\d{4})', folder_name)
    year = year_match.group(1) if year_match else str(Path().cwd().name)[:4]
    name = re.sub(r'\s*\d{4}\s*', '', folder_name).strip() or folder_name

    data = {
        'name': name,
        'year': year,
        'location': '',
        'artworks': []
    }

    for i, img in enumerate(images, 1):
        data['artworks'].append({
            'filename': img.name,
            'title': f"Image {i}",
            'year': year,
            'medium': '',
            'dimensions': ''
        })

    return data


def main():
    if len(sys.argv) < 2:
        print("=" * 55)
        print("Exhibition Generator for Michaela Mor's Website")
        print("=" * 55)
        print("\nUsage: python3 add-exhibition.py <exhibition_folder>")
        print("\nThe folder should contain:")
        print("  - Images (jpg, jpeg, png)")
        print("  - exhibition_data.txt (optional - will auto-generate if missing)")
        print("\nThe script will:")
        print("  1. Copy images to images/Gallery/[Exhibition Name]/")
        print("  2. Compress images (requires ImageMagick)")
        print("  3. Generate exhibition-X.html")
        print("  4. Update gallery.html")
        print("\nExample:")
        print("  python3 add-exhibition.py ~/Desktop/New_Exhibition_2025/")
        sys.exit(1)

    source_folder = Path(sys.argv[1]).resolve()

    if not source_folder.exists():
        print(f"Error: Folder not found: {source_folder}")
        sys.exit(1)

    if not source_folder.is_dir():
        print(f"Error: Not a directory: {source_folder}")
        sys.exit(1)

    print("=" * 55)
    print("Exhibition Generator for Michaela Mor's Website")
    print("=" * 55)
    print(f"\nSource folder: {source_folder}")

    # Find images
    images = find_images(source_folder)
    if not images:
        print("Error: No images found in folder")
        sys.exit(1)
    print(f"Found {len(images)} images")

    # Find or auto-generate data
    data_file = find_data_file(source_folder)
    if data_file:
        print(f"Found data file: {data_file.name}")
        data = parse_exhibition_file(data_file)
    else:
        print("No data file found - auto-generating from folder name")
        data = auto_generate_data(images, source_folder.name)

    if not data['name']:
        data['name'] = source_folder.name

    print(f"\nExhibition: {data['name']} ({data['year']})")
    print(f"Artworks: {len(data['artworks'])}")

    # Create destination folder
    dest_folder = SCRIPT_DIR / 'images' / 'Gallery' / data['name']
    print(f"\n[1/4] Copying images to: {dest_folder}")

    # Copy images
    copied_files = copy_images(source_folder, dest_folder, images)

    # Update artwork filenames if auto-generated
    if not data_file:
        data['artworks'] = []
        for i, filename in enumerate(copied_files, 1):
            data['artworks'].append({
                'filename': filename,
                'title': f"Image {i}",
                'year': data['year'],
                'medium': '',
                'dimensions': ''
            })

    # Compress images
    print(f"\n[2/4] Compressing images...")
    compress_images(dest_folder)

    # Get next exhibition number
    exhibition_num = get_next_exhibition_number()

    # Generate exhibition HTML
    print(f"\n[3/4] Creating exhibition-{exhibition_num}.html...")
    html = generate_exhibition_html(data, exhibition_num)

    output_file = SCRIPT_DIR / f"exhibition-{exhibition_num}.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  Created: {output_file.name}")

    # Update gallery.html
    print(f"\n[4/4] Updating gallery.html...")
    update_gallery_html(data, exhibition_num)
    print("  Updated: gallery.html")

    print(f"\n{'=' * 55}")
    print("SUCCESS!")
    print(f"{'=' * 55}")
    print(f"\nNew exhibition page: exhibition-{exhibition_num}.html")
    print(f"Images location: images/Gallery/{data['name']}/")
    print("\nNext steps:")
    print("  git add .")
    print(f"  git commit -m 'Add exhibition: {data['name']}'")
    print("  git push")


if __name__ == '__main__':
    main()
