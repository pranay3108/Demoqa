# utils/screenshot.py

import os
from datetime import datetime

def capture_screenshot(driver, name="screenshot"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{name}_{timestamp}.png"
    directory = "screenshots"

    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, filename)
    driver.save_screenshot(filepath)
    return filepath
