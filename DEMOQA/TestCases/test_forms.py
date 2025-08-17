from contextlib import nullcontext
from operator import truediv, is_not

import pytest
from Utilities.page_selector import pageselect, Submenuselectforfirsttime
from Pages.forms import Forms
from Utilities.setup import Setup

@pytest.fixture
def setup_data():
    driver = Setup().driver
    yield driver
    driver.quit()

def test_form(setup_data):
    driver = setup_data  # get driver from fixture
    Forms(driver)



