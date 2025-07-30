import logging
import pytest_check as check
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilities.excel_reader import fileread

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def Textbox(driver, workbook, sheet_name):
    """
    Fills out a dynamic text box form using data from Excel and validates the output display.

    :param driver: Selenium WebDriver instance
    :param workbook: openpyxl workbook object
    :param sheet_name: Sheet name containing form labels and data
    """
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    # Wait for page section matching sheet name
    wait.until(EC.visibility_of_element_located((By.XPATH, f"//h1[contains(text(),'{sheet_name}')]")))

    data = fileread(workbook, sheet_name)
    rows = len(data)
    columns = len(data[0])

    for i in range(1, rows):
        for j in range(columns):
            label = data[0][j]
            value = data[i][j]
            field_xpath = f"//label[contains(text(),'{label}')]/parent::div/following-sibling::div/*[self::input or self::textarea]"
            try:
                field = wait.until(EC.visibility_of_element_located((By.XPATH, field_xpath)))
                field.clear()
                field.send_keys(value)
                logger.info(f"✅ Filled field '{label}' with value '{value}'")
            except Exception as e:
                logger.error(f"⚠️ Failed to locate or fill field for label '{label}': {e}")
                continue  # Optional: skip and proceed to next field


        # Submit the form
        submit = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@id='submit']")))
        actions.move_to_element(submit).perform()
        driver.execute_script("arguments[0].click();", submit)
        logger.info("📤 Form submitted.")

        # Validate output values
        outputs = wait.until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@id='output']/div/p")))
        for output in outputs:
            driver.execute_script("arguments[0].scrollIntoView(true);", output)
            element_id = output.get_attribute("id").lower()
            actual = output.text.replace(" ", "").lower()

            for j in range(columns):
                header_key = data[0][j].replace(" ", "").lower()
                expected_value = data[i][j].replace(" ", "").lower()

                if element_id in header_key:
                    expected = f"{element_id}:{expected_value}"
                    logger.info(f"🔍 Checking field '{element_id}' | Expected: '{expected}' | Actual: '{actual}'")
                    check.equal(expected, actual, f"❌ Mismatch: expected '{expected}', got '{actual}'")
                    break
