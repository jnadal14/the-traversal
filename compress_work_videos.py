#!/usr/bin/env python3
"""Compress work videos - specifically for CLIPS/work/ directory"""

import os
import shutil
from moviepy import VideoFileClip

WORK_DIR = "/Users/jacob/Desktop/WEBSITE_TRAVERSAL/CLIPS/work"
BACKUP_DIR = "/Users/jacob/Desktop/WEBSITE_TRAVERSAL/CLIPS/work_backup"

def compress_work_videos():
    # Create backup
    if not os.path.exists(BACKUP_DIR):
        print(f"Creating backup in {BACKUP_DIR}/...")
        shutil.copytree(WORK_DIR, BACKUP_DIR)
        print("Backup complete!\n")
    
    # Get all video files
    videos = [f for f in os.listdir(WORK_DIR) if f.lower().endswith(('.mov', '.mp4'))]
    total = len(videos)
    
    print(f"Compressing {total} work videos...\n")
    
    for i, filename in enumerate(videos, 1):
        filepath = os.path.join(WORK_DIR, filename)
        original_size = os.path.getsize(filepath)
        
        # Skip if already small enough (< 5MB)
        if original_size < 5 * 1024 * 1024:
            print(f"[{i}/{total}] {filename} - already small ({original_size/1024/1024:.1f}MB), skipping")
            continue
        
        # Output filename
        base_name = os.path.splitext(filename)[0]
        temp_path = os.path.join(WORK_DIR, f"{base_name}_compressed.mp4")
        output_path = os.path.join(WORK_DIR, f"{base_name}.mp4")
        
        print(f"[{i}/{total}] {filename}...")
        
        try:
            # Load video
            clip = VideoFileClip(filepath)
            
            # Write compressed version WITH AUDIO (important for work videos!)
            clip.write_videofile(
                temp_path,
                codec='libx264',
                audio_codec='aac',
                audio_bitrate='128k',
                preset='medium',
                bitrate='1000k',  # 1Mbps target bitrate
                logger=None
            )
            clip.close()
            
            # Remove original and rename temp
            if os.path.exists(filepath):
                os.remove(filepath)
            os.rename(temp_path, output_path)
            
            new_size = os.path.getsize(output_path)
            reduction = (1 - new_size / original_size) * 100
            print(f"    {original_size/1024/1024:.1f}MB → {new_size/1024/1024:.1f}MB ({reduction:.0f}% smaller)\n")
            
        except Exception as e:
            print(f"    Error: {e}\n")
    
    print(f"\nDone! Originals backed up to: {BACKUP_DIR}/")

if __name__ == "__main__":
    compress_work_videos()

