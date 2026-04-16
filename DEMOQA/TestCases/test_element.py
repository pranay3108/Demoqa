from contextlib import nullcontext
from operator import truediv, is_not

import pytest
from Utilities.page_selector import pageselect, Submenuselectforfirsttime
from Pages.elements import Elements
from Utilities.setup import Setup

@pytest.fixture
def driver():
    driver = Setup().driver
    yield driver
    driver.quit()

def test_ele(driver):
    Elements(driver)
