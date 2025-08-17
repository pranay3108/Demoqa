import os
from contextlib import nullcontext
from operator import truediv, is_not
from openpyxl.reader.excel import load_workbook
import pytest

from Utilities.paths import TEST_DATA_DIR


def fileread(workbook,sheet_name):
    if sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]
        print(f"Selected sheet: {sheet.title}")
        data = []
        for row in sheet.iter_rows(values_only=True):
            # skip completely empty rows
            if any(cell is not None for cell in row):
                data.append(list(row))
        print("Multidimensional Array:", data)
    else:
        print(f"Sheet '{sheet_name}' not found in workbook!")

    return data



def workbookload(filename):
    file_path = os.path.join(TEST_DATA_DIR, filename+'.xlsx')
    # ✅ Load Workbook
    workbook = load_workbook(file_path)
    print("Workbook loaded from:", file_path)
    return workbook