#!/usr/bin/env python3
"""Compress images for web - reduces file size by ~90% while keeping quality"""

import os
import shutil
from PIL import Image

IMAGES_DIR = "IMAGES"
BACKUP_DIR = "IMAGES_BACKUP"
MAX_WIDTH = 2000
QUALITY = 82

def compress_images():
    # Create backup
    if not os.path.exists(BACKUP_DIR):
        print(f"Creating backup in {BACKUP_DIR}/...")
        shutil.copytree(IMAGES_DIR, BACKUP_DIR)
        print("Backup complete!")
    
    # Get all jpg files
    images = [f for f in os.listdir(IMAGES_DIR) if f.lower().endswith(('.jpg', '.jpeg'))]
    total = len(images)
    
    print(f"\nCompressing {total} images...\n")
    
    total_before = 0
    total_after = 0
    
    for i, filename in enumerate(images, 1):
        filepath = os.path.join(IMAGES_DIR, filename)
        
        # Get original size
        original_size = os.path.getsize(filepath)
        total_before += original_size
        
        # Open and resize
        with Image.open(filepath) as img:
            # Convert to RGB if necessary (for JPEG)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Resize if wider than MAX_WIDTH
            if img.width > MAX_WIDTH:
                ratio = MAX_WIDTH / img.width
                new_height = int(img.height * ratio)
                img = img.resize((MAX_WIDTH, new_height), Image.LANCZOS)
            
            # Save with compression
            img.save(filepath, 'JPEG', quality=QUALITY, optimize=True)
        
        # Get new size
        new_size = os.path.getsize(filepath)
        total_after += new_size
        
        reduction = (1 - new_size / original_size) * 100
        print(f"[{i}/{total}] {filename}: {original_size/1024/1024:.1f}MB → {new_size/1024:.0f}KB ({reduction:.0f}% smaller)")
    
    print(f"\n{'='*50}")
    print(f"TOTAL: {total_before/1024/1024:.1f}MB → {total_after/1024/1024:.1f}MB")
    print(f"SAVED: {(total_before-total_after)/1024/1024:.1f}MB ({(1-total_after/total_before)*100:.0f}% reduction)")
    print(f"{'='*50}")
    print(f"\nOriginals backed up to: {BACKUP_DIR}/")

if __name__ == "__main__":
    os.chdir("/Users/jacob/Desktop/WEBSITE_TRAVERSAL")
    compress_images()

