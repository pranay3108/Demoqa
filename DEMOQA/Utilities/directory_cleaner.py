import os
import shutil
import time


def clean_dir(download_dir):
    """
    Removes all files and subdirectories from the given download directory.
    """
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)  # Create it if it doesn't exist
        return

    for item in os.listdir(download_dir):
        item_path = os.path.join(download_dir, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except Exception as e:
            print(f"⚠️ Could not delete {item_path}: {e}")
