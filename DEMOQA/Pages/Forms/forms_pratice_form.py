import logging
import time

import pytest_check as check
from seleniumwire import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilities.excel_reader import fileread
from Utilities.date_picker import  select_date

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def PracticeForm(driver, workbook, sheet_name):
    actions = ActionChains(driver)
    wait = WebDriverWait(driver, 30)

    wait.until(EC.visibility_of_element_located((By.XPATH, f"//h1[contains(text(),'{sheet_name}')]")))
    wait.until(EC.visibility_of_element_located((By.XPATH, f"//h5[contains(text(),'Student Registration Form')]")))
    data = fileread(workbook, sheet_name)
    rows = len(data)
    columns = len(data[0])
    for i in range(1, rows):
        for j in range(columns):
            label = data[0][j]
            value = data[i][j]
            field_css=".mt-2"
            field_xpath="//div[contains(@class,'mt-2')]/div[1]"

            try:
                match label:
                    case "Name":
                        fields = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, field_css)))
                        for k in range(0,len(fields)):
                            field_name = fields[k].find_element(By.CSS_SELECTOR,".form-label").text
                            logger.info(
                                f"🔍 Checking field '{label}' | Expected: '{label}' | Actual: '{field_name}'")
                            check.equal(label, field_name, f"❌ Mismatch: expected '{label}', got '{field_name}'")
                            if label==field_name:
                                field_inputs = fields[k].find_elements(By.CSS_SELECTOR,".mr-sm-2")
                                parts = value.split()
                                for l in range(min(len(field_inputs), len(parts))):
                                    field_inputs[l].send_keys(parts[l])
                                    logger.info(f"✅ Filled field '{label}' with value '{value}'")
                                break
                            else:
                                continue

                    case "Gender":
                        fields = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, field_css)))
                        #special modification due error in code of gender
                        fields_xpath= wait.until(EC.visibility_of_all_elements_located((By.XPATH, field_xpath)))
                        for k in range(0, len(fields)):
                            field_name = fields_xpath[k].text
                            logger.info(
                                f"🔍 Checking field '{label}' | Expected: '{label}' | Actual: '{field_name}'")
                            check.equal(label, field_name, f"❌ Mismatch: expected '{label}', got '{field_name}'")
                            if label == field_name:
                                field_inputs = fields[k].find_elements(By.CSS_SELECTOR, ".custom-control-input")
                                field_checkbox_labels = fields[k].find_elements(By.CSS_SELECTOR,
                                                                                ".custom-control-label")
                                for l in range(min(len(field_inputs), len(field_checkbox_labels))):
                                    if value == field_checkbox_labels[l].text:
                                        driver.execute_script("arguments[0].scrollIntoView(true);", field_inputs[l])
                                        actions.move_to_element(field_inputs[l]).click().perform()
                                        logger.info(f"✅ Clicked radio button: '{field_checkbox_labels[l].text}'")
                                        logger.info(f"✅ Checked field '{label}' with value '{value}'")
                                        break
                                    else:
                                        continue

                                break
                            else:
                                continue
                        print()

                    case "Date of Birth":
                        fields = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, field_css)))
                        fields_xpath = wait.until(EC.visibility_of_all_elements_located((By.XPATH, field_xpath)))
                        for k in range(0, len(fields)):
                            field_name = fields_xpath[k].text
                            logger.info(
                                f"🔍 Checking field '{label}' | Expected: '{label}' | Actual: '{field_name}'")
                            check.equal(label, field_name, f"❌ Mismatch: expected '{label}', got '{field_name}'")
                            if label==field_name:
                                field_input = fields[k].find_element(By.CSS_SELECTOR, ".form-control")
                                driver.execute_script("arguments[0].scrollIntoView(true);", field_input)
                                field_input.send_keys("")
                                field_input.clear()
                                select_date(wait, value)
                    case "Subjects":
                        fields = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, field_css)))
                        for k in range(0, len(fields)):
                            field_name = fields[k].find_element(By.CSS_SELECTOR, ".form-label").text
                            logger.info(
                                f"🔍 Checking field '{label}' | Expected: '{label}' | Actual: '{field_name}'")
                            check.equal(label, field_name, f"❌ Mismatch: expected '{label}', got '{field_name}'")
                            if label == field_name:
                                
                        print()

                    case "Hobbies":
                        fields = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, field_css)))
                        for k in range(0,len(fields)):
                            field_name = fields[k].find_element(By.CSS_SELECTOR, ".form-label").text
                            logger.info(
                                f"🔍 Checking field '{label}' | Expected: '{label}' | Actual: '{field_name}'")
                            check.equal(label, field_name, f"❌ Mismatch: expected '{label}', got '{field_name}'")
                            if label==field_name:
                                field_inputs = fields[k].find_elements(By.CSS_SELECTOR, ".custom-control-input")
                                field_checkbox_labels = fields[k].find_elements(By.CSS_SELECTOR, ".custom-control-label")
                                for l in range(min(len(field_inputs), len(field_checkbox_labels))):
                                    if value==field_checkbox_labels[l].text :
                                        driver.execute_script("arguments[0].scrollIntoView(true);", field_inputs[l])
                                        actions.move_to_element(field_inputs[l]).click().perform()
                                        logger.info(f"✅ Clicked radio button: '{field_checkbox_labels[l].text}'")
                                        logger.info(f"✅ Checked field '{label}' with value '{value}'")
                                    else:
                                        continue

                                break
                            else:
                                continue




                    case "State and City":
                        print()
                    case _:
                        fields = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, field_css)))
                        fields_xpath = wait.until(EC.visibility_of_all_elements_located((By.XPATH, field_xpath)))
                        for k in range(0,len(fields)):
                            field_name = fields_xpath[k].text
                            #field_name = fields[k].find_element(By.CSS_SELECTOR,".form-label").text
                            logger.info(
                                f"🔍 Checking field '{label}' | Expected: '{label}' | Actual: '{field_name}'")
                            check.equal(label, field_name, f"❌ Mismatch: expected '{label}', got '{field_name}'")
                            if label==field_name:
                                field_inputs = fields[k].find_element(By.CSS_SELECTOR, ".mr-sm-2")
                                field_inputs.send_keys(value)
                                logger.info(f"✅ Filled field '{label}' with value '{value}'")
                                break
                            else:
                                continue
            

            except Exception as e:
                logger.error(f"⚠️ Failed to locate or fill field for label '{label}': {e}")
                continue

