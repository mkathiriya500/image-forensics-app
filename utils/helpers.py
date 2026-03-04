import os
import shutil
import hashlib

def cleanup_temp_files(files=None):
    """Clean up temporary files"""
    count = 0
    if files:
        for file in files:
            try:
                if os.path.exists(file):
                    os.remove(file)
                    count += 1
            except:
                pass
    return count

def setup_directories():
    """Create necessary directories"""
    dirs = ['temp', 'output', 'logs', 'cache']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)