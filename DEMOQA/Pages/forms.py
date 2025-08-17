from Pages.Forms.forms_pratice_form import PracticeForm
from Utilities.excel_reader import workbookload
from Utilities.page_selector import pageselect, Submenuselectforfirsttime


def Forms(driver):
    cardtobeselected = "Forms"
    pageselect(driver, cardtobeselected)
    workbook= workbookload(cardtobeselected)
    sheet_names = workbook.sheetnames
    for i in range (0,len(sheet_names)):
        print(sheet_names[i])
        submenutobeselected=sheet_names[i]
        Submenuselectforfirsttime(driver, submenutobeselected)
        match submenutobeselected:
            case "Practice Form":
                PracticeForm(driver, workbook, submenutobeselected)
            case _:
                print(f"Skipping unknown submenu: {submenutobeselected}")
                continue