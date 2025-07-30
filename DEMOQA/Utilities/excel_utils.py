import openpyxl

def getrow(file,sheetname):
    workbook= openpyxl.load_workbook(file)
    sheet=workbook.get_sheet_by_name(sheetname)
    return (sheet.max_row)