import logging
import pytest_check as check
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilities.excel_reader import fileread

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def CheckBox(driver, workbook, sheet_name):
    """
    Selects checkboxes based on Excel input and validates selected results.

    :param driver: Selenium WebDriver instance
    :param workbook: OpenPyXL workbook object
    :param sheet_name: Excel sheet name to read checkbox values from
    """
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    # Wait for correct section to appear
    wait.until(EC.visibility_of_element_located((By.XPATH, f"//h1[contains(text(),'{sheet_name}')]")))

    data = fileread(workbook, sheet_name)
    rows = len(data)

    # Expand all collapsible checkbox nodes
    while True:
        collapsed_nodes = driver.find_elements(By.CSS_SELECTOR, ".rct-node-collapsed .rct-collapse-btn")
        if not collapsed_nodes:
            break
        for node in collapsed_nodes:
            driver.execute_script("arguments[0].scrollIntoView(true);", node)
            actions.move_to_element(node).click().perform()
            wait.until(EC.staleness_of(node))  # Wait until node is updated

    # Select matching checkboxes
    checkbox_labels = driver.find_elements(By.CSS_SELECTOR, ".rct-title")

    for j in range(1, rows):
        checkbox_text = data[j][0].strip()
        found = False

        for checkbox in checkbox_labels:
            if checkbox.text.strip() == checkbox_text:
                driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                actions.move_to_element(checkbox).click().perform()
                logger.info(f"✅ Selected checkbox: '{checkbox_text}'")
                found = True
                break

        if not found:
            logger.warning(f"⚠️ Checkbox not found: '{checkbox_text}'")

    # Validate output section
    output_elements = wait.until(EC.visibility_of_all_elements_located(
        (By.XPATH, "//div[@id='result']/span[@class='text-success']")))

    for j in range(1, rows):
        expected = data[j][0].replace(".doc", "").strip().lower()
        logger.info(f"🔍 Verifying expected output: '{expected}'")

        match_found = False
        for output in output_elements:
            driver.execute_script("arguments[0].scrollIntoView(true);", output)
            actual = output.text.strip().lower()
            logger.info(f"   📘 Found output: '{actual}'")

            if expected == actual:
                logger.info(f"✅ Match confirmed for: '{expected}'")
                match_found = True
                break

        check.is_true(match_found, f"❌ Expected output '{expected}' not found.")
