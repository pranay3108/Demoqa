import logging
import time

import pytest_check as check
from seleniumwire import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilities.excel_reader import fileread

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def Links(driver, workbook, sheet_name):
    """
    Validates frontend links (including new tab links and API calls) using data from Excel.

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
            expected_text = data[i][j]
            if not expected_text or not str(expected_text).strip():
                logger.warning(f"⚠️ Skipping empty or invalid value at row {i}, column {j}")
                continue

            links = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//p/a")))

            # Handle links that open in new tab
            if "open new tab" in header:
                logger.info(f"🔗 Handling 'open new tab' link: '{expected_text}'")
                original_tabs = driver.window_handles
                link_url = None
                target = None

                for link in links:
                    if expected_text.strip() in link.text:
                        link_url = link.get_attribute("href")
                        target = link.get_attribute("target")
                        actions.move_to_element(link).perform()
                        driver.execute_script("arguments[0].click();", link)
                        break

                if target == "_blank":
                    wait.until(lambda d: len(d.window_handles) > len(original_tabs))
                    driver.switch_to.window(driver.window_handles[-1])
                    current_url = driver.current_url
                    logger.info(f"🆕 New tab opened: {current_url}")
                    check.equal(link_url, current_url, f"❌ URL mismatch in new tab")
                    driver.close()
                    driver.switch_to.window(original_tabs[0])
                else:
                    logger.warning(f"⚠️ Link did not open in new tab: '{expected_text}'")

            # Handle links that trigger an API call
            elif "api call" in header:
                logger.info(f"🔗 Handling 'API call' link: '{expected_text}'")
                for link in links:
                    if expected_text.strip() in link.text:
                        actions.move_to_element(link).perform()
                        driver.execute_script("arguments[0].click();", link)
                        time.sleep(2)  # Allow network calls to capture

                        matched = False
                        for request in driver.requests:
                            if "api/endpoint" in request.url and request.response:
                                api_status_code = request.response.status_code
                                api_status_reason = request.response.reason

                                logger.info(f"📡 API URL: {request.url}")
                                logger.info(f"✅ Status Code: {api_status_code}")
                                logger.info(f"✅ Reason: {api_status_reason}")

                                # Validate against frontend displayed response
                                frontend_status_code = driver.find_element(By.XPATH, "//p[@id='linkResponse']/b[1]").text
                                frontend_status_reason = driver.find_element(By.XPATH, "//p[@id='linkResponse']/b[2]").text

                                logger.info(f"🖥️ Frontend Status Code: {frontend_status_code}")
                                logger.info(f"🖥️ Frontend Reason: {frontend_status_reason}")

                                check.equal(str(api_status_code), frontend_status_code,
                                            f"❌ Status code mismatch")
                                check.equal(api_status_reason.strip(), frontend_status_reason.strip(),
                                            f"❌ Status reason mismatch")
                                matched = True
                                break

                        if not matched:
                            logger.error("❌ No matching API request found or response missing.")
                        break

            else:
                logger.warning(f"⚠️ Unhandled header: '{header}' at column {j}")
