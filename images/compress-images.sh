#!/bin/bash

# Michaela Mor Portfolio - Image Auto-Converter
# This script optimizes images for web display
# Usage: ./compress-images.sh [path-to-folder]

# Configuration
MAX_SIZE=1920          # Maximum dimension (width or height)
QUALITY=85             # JPEG quality (1-100, recommend 80-90)
STRIP_METADATA=true    # Remove EXIF data for privacy and smaller files

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Michaela Mor Portfolio${NC}"
echo -e "${BLUE}Image Compression Tool${NC}"
echo -e "${BLUE}================================${NC}\n"

# Get target directory
if [ -z "$1" ]; then
    echo -e "${YELLOW}No directory specified.${NC}"
    echo -e "Usage: ./compress-images.sh [path-to-folder]"
    echo -e "Example: ./compress-images.sh \"images/Gallery/New Exhibition\""
    exit 1
fi

TARGET_DIR="$1"

# Check if directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${YELLOW}Error: Directory not found: $TARGET_DIR${NC}"
    exit 1
fi

# Count images
IMAGE_COUNT=$(find "$TARGET_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | wc -l | tr -d ' ')

if [ "$IMAGE_COUNT" -eq 0 ]; then
    echo -e "${YELLOW}No images found in: $TARGET_DIR${NC}"
    exit 1
fi

echo -e "${GREEN}Found $IMAGE_COUNT images to compress${NC}"
echo -e "Target: ${MAX_SIZE}px max dimension, ${QUALITY}% quality\n"

# Get size before
SIZE_BEFORE=$(du -sh "$TARGET_DIR" | cut -f1)
echo -e "Current size: ${SIZE_BEFORE}\n"

# Process images
COUNTER=0
find "$TARGET_DIR" -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | while read -r file; do
    COUNTER=$((COUNTER + 1))
    FILENAME=$(basename "$file")
    echo -e "${BLUE}[$COUNTER/$IMAGE_COUNT]${NC} Compressing: $FILENAME"

    # Use 'magick' command (ImageMagick v7+)
    magick "$file" -resize "${MAX_SIZE}x${MAX_SIZE}>" -quality $QUALITY -strip "$file"
done

echo -e "\n${GREEN}✓ Compression complete!${NC}\n"

# Get size after
SIZE_AFTER=$(du -sh "$TARGET_DIR" | cut -f1)
echo -e "New size: ${SIZE_AFTER}"
echo -e "${GREEN}Ready to upload to website!${NC}\n"
