import logging
import os
import time

import pytest_check as check
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Utilities.directory_cleaner import clean_dir
from Utilities.excel_reader import fileread
from Utilities.paths import DOWNLOAD_DIR, TEST_DATA_DIR

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def UploadAndDownload(driver, workbook, sheet_name):
    """
    Automates file download and upload functionality based on Excel input.
    Validates download success and uploaded file name display.
    """
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    wait.until(EC.visibility_of_element_located((By.XPATH, f"//h1[contains(text(),'{sheet_name}')]")))

    data = fileread(workbook, sheet_name)
    rows = len(data)
    columns = len(data[0])

    # Clean download directory
    clean_dir(DOWNLOAD_DIR)
    logger.info("🧹 Download directory cleaned.")

    # Click Download button
    try:
        download_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Download')]")))
        actions.move_to_element(download_btn).perform()
        driver.execute_script("arguments[0].click();", download_btn)
        logger.info("📥 Download button clicked.")
    except Exception as e:
        logger.exception("❌ Failed to click download button.")
        return

    # Poll the download folder until the file is downloaded or timeout
    try:
        WebDriverWait(driver, 30, poll_frequency=1).until(
            lambda d: (
                    any(f.endswith(('.pdf', '.csv', '.xlsx', '.jpeg')) for f in os.listdir(DOWNLOAD_DIR))
                    and not any(f.endswith('.crdownload') for f in os.listdir(DOWNLOAD_DIR))
            )
        )
        logger.info("✅ File downloaded successfully.")
    except Exception:
        check.is_true(False, "❌ File download failed or timed out.")

    # Upload file(s)
    for i in range(1, rows):
        for j in range(columns):
            file_name = data[i][j]
            file_path = os.path.join(TEST_DATA_DIR, file_name)

            try:
                file_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
                file_input.send_keys(file_path)
                logger.info(f"📤 Uploaded file: {file_name}")

                # Get the frontend-displayed filename
                uploaded_text = wait.until(EC.visibility_of_element_located((By.ID, "uploadedFilePath"))).text
                logger.info(f"🧾 Frontend displays: {uploaded_text}")

                uploaded_filename = os.path.basename(uploaded_text)
                check.equal(uploaded_filename, file_name, f"❌ File name mismatch: expected '{file_name}', got '{uploaded_filename}'")
            except Exception as e:
                logger.exception(f"⚠️ Failed to upload or validate file: {file_name}")
                continue

    # Final cleanup
    clean_dir(DOWNLOAD_DIR)
    logger.info("🧼 Download directory cleaned after upload validation.")
