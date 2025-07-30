import logging
import time

import pytest_check as check
import requests
from seleniumwire import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilities.excel_reader import fileread

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def DynamicProperties(driver, workbook, sheet_name):
    print("b")
