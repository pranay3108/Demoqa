import logging
import time
from urllib.parse import urlparse
import pytest_check as check
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilities.excel_reader import fileread

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def BrokenLinksImages(driver, workbook, sheet_name):
    """
    Validates valid & broken images as well as links using data from Excel.

    :param driver: Selenium WebDriver instance with Selenium Wire enabled
    :param workbook: openpyxl workbook object
    :param sheet_name: Sheet name containing link types and expected data
    """
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 30)

    wait.until(EC.visibility_of_element_located((By.XPATH, f"//h1[contains(text(),'{sheet_name}')]")))

    data = fileread(workbook, sheet_name)
    rows = len(data)
    columns = len(data[0])

    for j in range(columns):
        header = data[0][j].lower()

        for i in range(1, rows):
            match header:
                case "images":
                    label_text = data[i][j]
                    xpath = f"//p[contains(text(),'{label_text}')]/following-sibling::*[1][self::img]"
                    src = ""

                    try:
                        img = driver.find_element(By.XPATH, xpath)
                        src = img.get_attribute("src")
                        logger.info(f"{label_text} -> {src}")
                    except Exception as e:
                        logger.warning(f"Could not find image for label '{label_text}': {e}")
                        continue

                    if not src:
                        logger.warning("Image with no src attribute.")
                        continue

                    # Check if image is visually broken by naturalWidth === 0
                    is_broken = driver.execute_script("return arguments[0].naturalWidth === 0", img)
                    if is_broken:
                        logger.info(f"Visually broken image: {src}")
                        check.equal(label_text.strip().lower(), "broken image")
                    else:
                        logger.info(f"Visually valid image: {src}")
                        check.equal(label_text.strip().lower(), "valid image")

                case "links":
                    label_text = data[i][j]
                    xpath = f"//a[contains(text(),'{label_text}')]"
                    try:
                        link = driver.find_element(By.XPATH, xpath)
                    except Exception as e:
                        logger.warning(f"Link with label '{label_text}' not found: {e}")
                        continue

                    link_url = link.get_attribute("href")
                    parsed_link_url = urlparse(link_url)
                    normalized_link_url = parsed_link_url.netloc + parsed_link_url.path

                    # Clear previous requests to get fresh network calls
                    driver.requests.clear()
                    actions.move_to_element(link).perform()
                    driver.execute_script("arguments[0].click();", link)
                    time.sleep(5)  # Wait for requests to complete

                    link_checked = False

                    for request in driver.requests:
                        if not request.response:
                            continue
                        parsed_req_url = urlparse(request.url)
                        normalized_req_url = parsed_req_url.netloc + parsed_req_url.path

                        if normalized_req_url == normalized_link_url:
                            status_code = request.response.status_code
                            logger.info(f"URL: {normalized_req_url} - Status: {status_code}")

                            if status_code != 200:
                                logger.error(f"❌ Broken link code: {status_code}")
                                check.equal(label_text.strip(), "Broken Link")
                            else:
                                logger.info("✅ Link is working")
                                current_url = driver.current_url
                                parsed_current_url = urlparse(current_url)
                                normalized_current_url = parsed_current_url.netloc + parsed_current_url.path
                                check.equal(normalized_current_url, normalized_link_url)
                                check.equal(label_text.strip(), "Valid Link")

                            link_checked = True
                            driver.back()
                            break

                    if not link_checked:
                        logger.error(f"❌ No matching network request found for link labeled '{label_text}'.")
                        driver.back()
