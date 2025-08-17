import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Downloads folder
DOWNLOAD_DIR = os.path.join(BASE_DIR, 'downloads')

# Test data
TEST_DATA_DIR = os.path.join(BASE_DIR, 'Testdata')

# Logs
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# Example file
SAMPLE_EXCEL = os.path.join(TEST_DATA_DIR, 'sample.xlsx')
