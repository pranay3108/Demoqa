import logging
import pytest_check as check
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilities.excel_reader import fileread
from Utilities.table_reader import tableread

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def WebTables(driver, workbook, sheet_name):
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 10)

    wait.until(EC.visibility_of_element_located((By.XPATH, f"//h1[contains(text(),'{sheet_name}')]")))
    data = fileread(workbook, sheet_name)
    rows, cols = len(data), len(data[0])

    # ➕ Add entries
    for i in range(1, rows):
        add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add')]")))
        driver.execute_script("arguments[0].scrollIntoView(true);", add_btn)
        actions.move_to_element(add_btn).click().perform()

        for j in range(cols):
            field = wait.until(EC.visibility_of_element_located((
                By.XPATH, f"//label[contains(text(),'{data[0][j]}')]/parent::div/following-sibling::div/*[self::input or self::textarea]"
            )))
            field.send_keys(data[i][j])

        submit = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
        actions.move_to_element(submit).click().perform()
        logger.info(f"✅ Added row: {data[i]}")

    # 📋 Validate table data
    tabledata = tableread(driver)

    # 🔍 Search, Edit, Delete
    for i in range(1, rows):
        search_box = wait.until(EC.visibility_of_element_located((By.ID, "searchBox")))
        search_box.clear()
        search_box.send_keys(data[i][0])

        row_elems = wait.until(EC.visibility_of_all_elements_located(
            (By.XPATH, "//div[contains(@class,'rt-tr-group')]")
        ))
        cells = row_elems[0].find_elements(By.CSS_SELECTOR, "div.rt-td")
        original_value = data[i][0]

        # 🔎 Verify search result
        logger.info(f"🔍 Searching for: {original_value}")
        check.equal(cells[0].text.strip(), original_value, f"Expected value '{original_value}' not found.")

        # Find action column index
        headers = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".rt-resizable-header-content")))
        action_index = next((idx for idx, h in enumerate(headers) if h.text.strip() == "Action"), -1)

        if action_index == -1:
            logger.error("❌ 'Action' column not found.")
            return

        # ✏️ Edit row
        edit_icon = cells[action_index].find_element(By.XPATH, ".//span[@title='Edit']")
        driver.execute_script("arguments[0].scrollIntoView(true);", edit_icon)
        edit_icon.click()

        first_field = wait.until(EC.visibility_of_element_located((
            By.XPATH, f"//label[contains(text(),'{data[0][0]}')]/parent::div/following-sibling::div/*[self::input or self::textarea]"
        )))
        first_field.clear()
        edited_value = original_value + "-Edited"
        first_field.send_keys(edited_value)

        submit = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
        submit.click()

        # 🔁 Verify edit
        search_box = wait.until(EC.visibility_of_element_located((By.ID, "searchBox")))
        search_box.clear()
        search_box.send_keys(edited_value)

        row_elems = wait.until(EC.visibility_of_all_elements_located(
            (By.XPATH, "//div[contains(@class,'rt-tr-group')]")
        ))
        edited_cell_text = row_elems[0].find_elements(By.CSS_SELECTOR, "div.rt-td")[0].text.strip()
        logger.info(f"✏️ Edited cell: {edited_cell_text}")
        check.equal(edited_cell_text, edited_value, f"Expected '{edited_value}' after edit.")

        # 🗑️ Delete entry
        delete_icon = row_elems[0].find_elements(By.CSS_SELECTOR, "div.rt-td")[action_index].find_element(
            By.XPATH, ".//span[@title='Delete']"
        )
        delete_icon.click()

        # Verify deletion
        search_box = wait.until(EC.visibility_of_element_located((By.ID, "searchBox")))
        search_box.send_keys(Keys.CONTROL, 'a')
        search_box.send_keys(Keys.BACKSPACE)

        search_box.send_keys(edited_value)
        deleted_rows = driver.find_elements(By.XPATH, "//div[contains(@class,'rt-tr-group')]")
        for row in deleted_rows:
            cell_text = row.find_elements(By.CSS_SELECTOR, "div.rt-td")[0].text.strip()
            check.not_equal(cell_text, edited_value, f"'{edited_value}' was not deleted.")
            logger.info(f"🗑️ Deleted entry check: '{cell_text}' != '{edited_value}'")
