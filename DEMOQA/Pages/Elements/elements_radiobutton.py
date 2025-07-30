import logging
import pytest_check as check
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilities.excel_reader import fileread

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def RadioButton(driver, workbook, sheet_name):
    """
    Selects radio buttons based on Excel input and verifies selection success.

    :param driver: Selenium WebDriver instance
    :param workbook: openpyxl workbook object
    :param sheet_name: Sheet name containing radio options to select
    """
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    # Wait for page title
    wait.until(EC.visibility_of_element_located((By.XPATH, f"//h1[contains(text(),'{sheet_name}')]")))

    data = fileread(workbook, sheet_name)

    # Get all radio buttons and their corresponding labels
    radio_inputs = driver.find_elements(By.XPATH, "//input[@type='radio']")
    radio_labels = driver.find_elements(By.XPATH, "//input[@type='radio']/following-sibling::label")

    for i in range(len(data)):
        expected_option = data[i][0].strip()
        logger.info(f"🔘 Selecting radio option: '{expected_option}'")

        match_found = False

        for j in range(len(radio_labels)):
            label_text = radio_labels[j].text.strip()

            if label_text == expected_option:
                match_found = True
                class_attr = radio_inputs[j].get_attribute("class")

                if 'disabled' in class_attr:
                    logger.info(f"🚫 Radio option '{label_text}' is disabled.")
                    check.equal(label_text, "No", f"Disabled option should be 'No', but got '{label_text}'")
                else:
                    driver.execute_script("arguments[0].scrollIntoView(true);", radio_inputs[j])
                    actions.move_to_element(radio_inputs[j]).click().perform()
                    logger.info(f"✅ Clicked radio button: '{label_text}'")

                    # Validate the success message
                    success_text = wait.until(
                        EC.visibility_of_element_located(
                            (By.XPATH, "//p/span[@class='text-success']")
                        )
                    ).text.strip()

                    logger.info(f"📘 Success text displayed: '{success_text}'")
                    check.equal(label_text, success_text,
                                f"❌ Mismatch: selected '{label_text}', but displayed '{success_text}'")
                break

        if not match_found:
            logger.warning(f"⚠️ Radio option '{expected_option}' not found on the page.")
            check.is_true(False, f"Radio option '{expected_option}' not found.")
