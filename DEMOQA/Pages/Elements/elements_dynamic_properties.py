import logging
import time

import pytest_check as check
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilities.excel_reader import fileread

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def DynamicProperties(driver, workbook, sheet_name):
    """
    Tests dynamic UI behaviors: enable, visible, and color-change buttons.
    Validates interaction timing and appearance based on Excel-driven navigation.

    :param driver: Selenium WebDriver instance
    :param workbook: openpyxl workbook object
    :param sheet_name: Sheet name used for section identification
    """
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 30)

    # Wait for the page section with matching sheet name to load
    wait.until(EC.visibility_of_element_located((By.XPATH, f"//h1[contains(text(),'{sheet_name}')]")))

    # --- COLOR CHANGE BUTTON ---
    try:
        driver.get("https://demoqa.com/dynamic-properties")
        color_button = driver.find_element(By.ID, "colorChange")
        initial_color = color_button.value_of_css_property("color")
        start_color = time.perf_counter()
        # Wait for the color to change
        wait.until(lambda d: d.find_element(By.ID, "colorChange").value_of_css_property("color") != initial_color)
        end_color = time.perf_counter()
        new_color = color_button.value_of_css_property("color")
        color_duration = round(end_color - start_color, 2)
        logger.info(f"🎨 Initial button color: {initial_color}")
        logger.info(f"🎨 Color changed to: {new_color} after {color_duration} seconds.")
        check.not_equal(initial_color, new_color, "❌ Color did not change.")
    except Exception as e:
        logger.exception("❌ Failed to detect color change.")
        check.is_true(False, "❌ Color Change test failed.")

    # --- ENABLED AFTER BUTTON ---
    try:
        driver.refresh()
        start_enabled = time.perf_counter()
        enabled_btn = wait.until(EC.element_to_be_clickable((By.ID, "enableAfter")))
        end_enabled = time.perf_counter()
        enabled_duration = round(end_enabled - start_enabled, 2)
        enabled_btn.click()
        logger.info(f"✅ 'Enable After' button clicked after {enabled_duration} seconds.")
        check.is_true(enabled_btn.is_enabled(), "❌ Enable After button was not clickable.")
    except Exception as e:
        logger.exception("❌ Failed to click 'Enable After' button.")
        check.is_true(False, "❌ Enable After button test failed.")

    # --- VISIBLE AFTER BUTTON ---
    try:
        driver.refresh()
        start_visible = time.perf_counter()
        visible_btn = wait.until(EC.visibility_of_element_located((By.ID, "visibleAfter")))
        end_visible = time.perf_counter()

        visible_duration = round(end_visible - start_visible, 2)
        visible_btn.click()
        logger.info(f"✅ 'Visible After' button clicked after {visible_duration} seconds.")
        check.is_true(visible_btn.is_displayed(), "❌ Visible After button was not visible.")
    except Exception as e:
        logger.exception("❌ Failed to click 'Visible After' button.")
        check.is_true(False, "❌ Visible After button test failed.")
