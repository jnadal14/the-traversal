#!/usr/bin/env python3
"""Compress videos for web - converts .mov to compressed .mp4"""

import os
import shutil
from moviepy import VideoFileClip

CLIPS_DIR = "CLIPS"
BACKUP_DIR = "CLIPS_BACKUP"

def compress_videos():
    os.chdir("/Users/jacob/Desktop/WEBSITE_TRAVERSAL")
    
    # Create backup
    if not os.path.exists(BACKUP_DIR):
        print(f"Creating backup in {BACKUP_DIR}/...")
        shutil.copytree(CLIPS_DIR, BACKUP_DIR)
        print("Backup complete!\n")
    
    # Get all video files
    videos = [f for f in os.listdir(CLIPS_DIR) if f.lower().endswith(('.mov', '.mp4'))]
    total = len(videos)
    
    print(f"Compressing {total} videos...\n")
    
    total_before = 0
    total_after = 0
    
    for i, filename in enumerate(videos, 1):
        filepath = os.path.join(CLIPS_DIR, filename)
        original_size = os.path.getsize(filepath)
        total_before += original_size
        
        # Output filename (always .mp4)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(CLIPS_DIR, f"{base_name}.mp4")
        temp_path = os.path.join(CLIPS_DIR, f"{base_name}_temp.mp4")
        
        print(f"[{i}/{total}] {filename}...")
        
        try:
            # Load video
            clip = VideoFileClip(filepath)
            
            # Write compressed version (no audio for gallery loops)
            clip.write_videofile(
                temp_path,
                codec='libx264',
                audio=False,
                preset='medium',
                ffmpeg_params=['-crf', '26'],
                logger=None  # Suppress verbose output
            )
            clip.close()
            
            # Remove original and rename temp
            if os.path.exists(filepath) and filepath != output_path:
                os.remove(filepath)
            if os.path.exists(output_path) and output_path != temp_path:
                os.remove(output_path)
            os.rename(temp_path, output_path)
            
            new_size = os.path.getsize(output_path)
            total_after += new_size
            
            reduction = (1 - new_size / original_size) * 100
            print(f"    {original_size/1024/1024:.1f}MB → {new_size/1024/1024:.1f}MB ({reduction:.0f}% smaller)")
            
        except Exception as e:
            print(f"    Error: {e}")
            total_after += original_size
    
    print(f"\n{'='*50}")
    print(f"TOTAL: {total_before/1024/1024:.1f}MB → {total_after/1024/1024:.1f}MB")
    print(f"SAVED: {(total_before-total_after)/1024/1024:.1f}MB ({(1-total_after/total_before)*100:.0f}% reduction)")
    print(f"{'='*50}")
    print(f"\nOriginals backed up to: {BACKUP_DIR}/")
    print("\nNOTE: All .mov files converted to .mp4 - update index.html references!")

if __name__ == "__main__":
    compress_videos()

