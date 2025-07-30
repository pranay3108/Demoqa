import logging
import pytest_check as check
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilities.excel_reader import fileread

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def Buttons(driver, workbook, sheet_name):
    """
    Performs button interactions (double click, right click, normal click)
    and validates corresponding success messages.
    """
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    # Wait for section to load
    wait.until(EC.visibility_of_element_located(
        (By.XPATH, f"//h1[contains(text(),'{sheet_name}')]")
    ))

    data = fileread(workbook, sheet_name)  # Not currently used, but kept for consistency
    buttons = driver.find_elements(By.XPATH, "//button[contains(@class,'btn')]")

    for button in buttons:
        button_text = button.text.strip()
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        actions.move_to_element(button)

        logger.info(f"🟦 Interacting with button: '{button_text}'")

        match button_text:
            case "Double Click Me":
                actions.double_click(button).perform()
                message_elem = wait.until(EC.visibility_of_element_located(
                    (By.ID, "doubleClickMessage")
                ))
                message = message_elem.text
                logger.info(f"✅ Double click message: '{message}'")
                check.is_in("double click", message.lower())

            case "Right Click Me":
                actions.context_click(button).perform()
                message_elem = wait.until(EC.visibility_of_element_located(
                    (By.ID, "rightClickMessage")
                ))
                message = message_elem.text
                logger.info(f"✅ Right click message: '{message}'")
                check.is_in("right click", message.lower())

            case "Click Me":
                actions.click(button).perform()
                message_elem = wait.until(EC.visibility_of_element_located(
                    (By.ID, "dynamicClickMessage")
                ))
                message = message_elem.text
                logger.info(f"✅ Dynamic click message: '{message}'")
                check.is_in("dynamic click", message.lower())

            case _:
                logger.warning(f"⚠️ Unrecognized button: '{button_text}'")
