import time
from openpyxl.reader.excel import load_workbook
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
#
def tableread(driver):
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 10)
    tabledata = []

    # Step 1: Read header row
    tableheader = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.rt-resizable-header-content'))
    )
    header_row = [cell.text.strip() for cell in tableheader]
    tabledata.append(header_row)  # Add header as first row

    # Step 2: Read all table rows page by page
    nextbutton = True
    while nextbutton:
        # Wait for visible table rows
        rows = wait.until(
            EC.visibility_of_all_elements_located((By.XPATH, "//div[contains(@class,'rt-tr-group')]"))
        )

        # Step 3: Loop through visible rows and extract cell data
        for row in rows:
            cells = row.find_elements(By.CSS_SELECTOR, "div.rt-td")
            if not cells:
                continue  # skip if no cells found

            first_cell_text = cells[0].text.strip()
            if first_cell_text == "":
                continue  # skip the row if first cell is empty or only whitespace

            # Collect all cell data for the row
            row_data = [cell.text.strip() for cell in cells]
            tabledata.append(row_data)


        # Step 4: Check if 'Next' button is disabled
        next_button = driver.find_element(By.XPATH, "//button[text()='Next']")
        if next_button.get_attribute("disabled"):
            nextbutton = False
        else:
            next_button.click()

    return tabledata


