from openpyxl.reader.excel import load_workbook

from Pages.Elements.elements_broken_links_Images import BrokenLinksImages
from Pages.Elements.elements_dynamic_properties import DynamicProperties
from Pages.Elements.elements_links import Links
from Utilities.page_selector import pageselect, Submenuselectforfirsttime
from Utilities.excel_reader import fileread,workbookload
from Pages.Elements.elements_textbox import Textbox
from Pages.Elements.elements_checkbox import CheckBox
from Pages.Elements.elements_radiobutton import RadioButton
from Pages.Elements.elements_webtables import WebTables
from Pages.Elements.elements_buttons import Buttons
from Pages.Elements.elements_upload_and_download import UploadandDownload




def Elements(driver):
    cardtobeselected = "Elements"
    pageselect(driver, cardtobeselected)
    workbook= workbookload(cardtobeselected)
    sheet_names = workbook.sheetnames
    for i in range (0,len(sheet_names)):
        print(sheet_names[i])
        submenutobeselected=sheet_names[i]
        Submenuselectforfirsttime(driver, submenutobeselected)
        match submenutobeselected:
            case "Text Box1":
                Textbox(driver, workbook, submenutobeselected)
            case "Check Box1":
                CheckBox(driver, workbook, submenutobeselected)
            case "Radio Button1":
                RadioButton(driver, workbook, submenutobeselected)
            case "Web Tables1":
                WebTables(driver, workbook, submenutobeselected)
            case "Buttons1":
                Buttons(driver, workbook, submenutobeselected)
            case "Links1":
                Links(driver, workbook, submenutobeselected)
            case "Broken Links - Images":
                BrokenLinksImages(driver, workbook, submenutobeselected)
            case "Upload and Download":
                UploadandDownload(driver, workbook, submenutobeselected)
            case "Dynamic Properties":
                DynamicProperties(driver, workbook, submenutobeselected)
            case _:
                print(f"Skipping unknown submenu: {submenutobeselected}")
                continue




































