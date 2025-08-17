import logging
from seleniumwire import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# XPaths
DATEPICKER_XPATH = "//div[@class='react-datepicker']"
YEAR_XPATH = "//select[@class='react-datepicker__year-select']"
MONTH_XPATH = "//select[@class='react-datepicker__month-select']"
DAY_XPATH = "//div[contains(@class,'react-datepicker__day ')]"

OUTSIDE_MONTH_CLASS = "react-datepicker__day--outside-month"


def select_date(wait: WebDriverWait, value):
    """
    Select a date from a React Datepicker component.

    Args:
        wait (WebDriverWait): Selenium WebDriverWait instance.
        value (datetime): Python datetime object with year, month, and day.
    """
    try:
        # Extract year, month, day
        year = str(value.year)
        month = str(value.month - 1)  # Adjust because datepicker months are 0-based
        day = str(value.day)

        # Ensure datepicker is visible
        wait.until(EC.visibility_of_element_located((By.XPATH, DATEPICKER_XPATH)))

        # Select Year
        year_dropdown = wait.until(EC.visibility_of_element_located((By.XPATH, YEAR_XPATH)))
        Select(year_dropdown).select_by_value(year)
        logger.info(f"✅ Selected Year: {year}")

        # Select Month
        month_dropdown = wait.until(EC.visibility_of_element_located((By.XPATH, MONTH_XPATH)))
        Select(month_dropdown).select_by_value(month)
        logger.info(f"✅ Selected Month (0-based): {month}")

        # Select Day
        days_elements = wait.until(EC.visibility_of_all_elements_located((By.XPATH, DAY_XPATH)))
        for day_element in days_elements:
            class_attr = day_element.get_attribute("class")
            if OUTSIDE_MONTH_CLASS in class_attr:
                continue
            if day_element.text == day:
                day_element.click()
                logger.info(f"✅ Selected Day: {day}")
                return
        else:
            logger.error(f"❌ Could not find valid day: {day}")

    except Exception as e:
        logger.exception(f"⚠️ Error while selecting date {value}: {e}")
