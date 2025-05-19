from enum import Enum
import argparse as ap
import re

import pyautogui as pag
import pyperclip as ppc
import psutil as pu
import pyinputplus as pyip


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

RESOURCE_PATH = "./resources"


class Methods(Enum):
    HTML = 0
    XLS = 1
    Registry_1 = 2
    Registry_2 = 3


def FindImageNonCentered(image_path: str):
    try:
        (top, left, _) = tuple(pag.locateOnScreen(f"{RESOURCE_PATH}/{image_path}"))
        return (top, left)

    except pag.ImageNotFoundException:
        return None


def FindImage(image_path: str):
    try:
        (top, left, w, h) = tuple(pag.locateOnScreen(f"{RESOURCE_PATH}/{image_path}"))
        return (top + w // 2, left + h // 2)

    except pag.ImageNotFoundException:
        return None


def FindAnyImages(image_paths: list[str]):
    for image_path in image_paths:
        image = FindImage(image_path)

        if image is not None:
            return image


def FindProcess(name: str):
    search_string = f"{name}.exe"

    for process in pu.process_iter():
        if re.match(search_string.lower(), process.name().lower()):
            return process

    return None


def FindImageAndClick(image_path: str):
    coordinates = FindImage(image_path)

    if coordinates is None:
        return

    ClickButton(coordinates[0], coordinates[1])
    return


def ClickYesButton():
    coordinates = FindImage("yes_1.png"), FindImage("yes_2.png")

    if (coordinates[0] is not None) or (coordinates[1] is not None):
        pag.press("enter")

    return


def CenterCursor():
    pag.moveTo(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


def FindItemInList(item_name: str):
    pag.hotkey("home")

    found = False
    name = ""
    prev = ""
    while not found:
        prev = name
        pag.press("down")
        pag.hotkey(["ctrl", "c"])

        name = ppc.paste()

        if re.search(item_name.strip(), name.strip(), re.IGNORECASE):
            found = True
            break

        if name == prev:
            break

    return found


def ChooseSaveMethod(method_number: Methods):
    for _ in range(method_number):
        pag.press("down")

    pag.press("enter")

    return


def WaitProcess(process: pu.Process):
    process_percent = process.cpu_percent(3)

    while process_percent := process.cpu_percent(3):
        if process_percent > 1:
            pag.sleep(1)
        else:
            break
    
    return


def DoubleClickButton(x: int, y: int):
    pag.moveTo(x, y, duration=0.25)
    pag.doubleClick()

    return


def ClickButton(x: int, y: int):
    pag.moveTo(x, y, duration=0.25)
    pag.click()

    return


def ChooseSaveMode(input_str: str):
    if input_str == "html":
        return Methods.HTML
    elif input_str == "xls":
        return Methods.XLS
    elif input_str == "reg_1":
        return Methods.Registry_1
    elif input_str == "reg_2":
        return Methods.Registry_2


def ChoosePriemka(priemka_number):
    ClickButton(1129, 124)

    pag.sleep(0.75)
    pag.press("delete")

    FindImageAndClick("add_button.png")

    pag.sleep(0.75)
    pag.press("left")

    pag.sleep(2.5)
    pag.press("home")

    FindItemInList(priemka_number)
    pag.press("enter")
    pag.hotkey("alt", "f4")

    FindImageAndClick("OK_button.png")
    ClickYesButton()
    
    FindImageAndClick("OK_but.png")
    
    
def chooseVariant(process : pu.Process):
    pag.sleep(0.75)
    FindImageAndClick("choose_variants.png")
    
    pag.sleep(2)

    coordinate = (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2)
    ClickButton(*coordinate)
    WaitProcess(process)

    pag.press("home")
    if FindItemInList("Список 1 этап"):
        pag.press("enter")
        
    return

def FormatActivate(process : pu.Process):
    ClickButton(494, 155)
    
    format_activate = FindImage("check_foramt_list_1.jpg")
    
    pag.moveTo(*format_activate)
    pag.move(175, 0)
    
    pag.sleep(2.25)
    pag.click()
    
    pag.sleep(0.75)
    FindImageAndClick("create_button.jpg")
    WaitProcess(process)


def ParseCommandLineArgs():
    parser = ap.ArgumentParser("create_concurce_spiski")
    
    parser.add_argument("priemka_number", type=int)
    parser.add_argument("save_mode", type=str, default="html")
    parser.add_argument("--need_choose_variant", type=bool, action="store_true")
    
    return parser.parse_args()


def OpenMaster(process_need: str, priemka_number: str, save_mode: str, choose_variant: bool = False):
    save_mode = ChooseSaveMode(save_mode)
    print("Бот заработает через 5 секунд. Откройте 1С...")

    process = FindProcess(process_need)

    pag.sleep(2.25)
    FindImageAndClick("priemka_button.png")
    pag.sleep(2.25)
    FindImageAndClick("List_master_button.png")

    pag.sleep(5)
    pag.moveTo(1819, 82, duration=0.5)
    pag.click()

    if choose_variant:
       chooseVariant(process) 

    ChoosePriemka(priemka_number)

    FormatActivate(process)
    
    pag.sleep(1.5)
    pag.sleep(0.5)
    ClickButton(547, 81)

    pag.sleep(0.75)
    ChooseSaveMethod(save_mode.value)

    pag.sleep(0.75)
    ClickButton(1255, 153)

    pag.sleep(1.25)
    ClickButton(365, 230)

    pag.sleep(2)




def main():
    arguments = ParseCommandLineArgs()
    OpenMaster("1cv8c", arguments.priemka_number, arguments.save_mode, arguments.need_choose_variant)


if __name__ == "__main__":
    main()
