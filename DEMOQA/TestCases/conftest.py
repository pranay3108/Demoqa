# conftest.py

import pytest
import pytest_html
from Utilities.screenshot import capture_screenshot
import os

# For pytest-html
def pytest_configure(config):
    if hasattr(config, '_metadata'):
        config._metadata['Project Name'] = 'Your Automation Project'
        config._metadata['Module'] = 'DEMOQA'
        config._metadata['Tester'] = 'Your Name'


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Yield to let other hooks run
    outcome = yield
    report = outcome.get_result()

    # Only take screenshot if the test failed
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            filepath = capture_screenshot(driver, item.name)
            if hasattr(report, "extra"):
                report.extra.append(pytest_html.extras.image(filepath))
            else:
                report.extra = [pytest_html.extras.image(filepath)]
