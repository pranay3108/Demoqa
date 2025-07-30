import time
from argparse import Action

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from Utilities.setup import Setup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def pageselect(driver,Cardtobeselected):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//a")))
    driver.execute_script("window.scrollBy(0, 500);")
    Cards = driver.find_elements(By.CSS_SELECTOR, ".top-card")
    Cardnames = driver.find_elements(By.XPATH, "//div[contains(@class,'top-card')]//preceding::h5")
    print(len(Cardnames))
    for i in range(0, len(Cardnames)):
        if Cardnames[i].text == Cardtobeselected:
            Cards[i].click()
            break

    #element=wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'"+Cardtobeselected+"')]/parent::div")))
    #actions = ActionChains(driver)
    #Perform mouse hover and click on the element
    #actions.move_to_element(element).click().perform()





def Submenuselectforfirsttime(driver,submenutobeselected):
    wait = WebDriverWait(driver, 10)
    actions = ActionChains(driver)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'show')]/descendant::li")))
    Submenulist = driver.find_elements(By.XPATH, "//div[contains(@class,'show')]/descendant::li")
    for i in range(0, len(Submenulist)):
        if Submenulist[i].text == submenutobeselected:
            # Perform mouse hover and click on the element
            ele = Submenulist[i]
            wait.until(EC.element_to_be_clickable(ele))
            time.sleep(5)
            driver.execute_script("arguments[0].scrollIntoView(true);", ele)
            actions.move_to_element(ele).click().perform()
            break













