import re

import pyautogui as pag
import pyperclip as ppc
import psutil as pu

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

RESOURCE_PATH = "./resources"


def FindImage(image_path: str):
    try:
        (top, left, w, h) = tuple(pag.locateOnScreen(f"{RESOURCE_PATH}/{image_path}"))
        return (top + w // 2, left + h // 2)

    except pag.ImageNotFoundException:
        return None


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


def CenterCursor():
    pag.moveTo(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


def FindItemInList(item_name: str):
    pag.hotkey("home")

    found = False
    name = ""
    while not found:
        pag.press("down")
        pag.hotkey("ctrl", "c")

        name = ppc.paste()

        if re.search(item_name.strip(), name.strip(), re.IGNORECASE):
            found = True
            break

    return found


def WaitProcess(process: pu.Process):
    process_percent = process.cpu_percent()

    while process_percent := process.cpu_percent(3):
        pag.sleep(1.5)

    return


def DoubleClickButton(x: int, y: int):
    pag.moveTo(x, y, duration=0.25)
    pag.doubleClick()

    return


def ClickButton(x: int, y: int):
    pag.moveTo(x, y, duration=0.25)
    pag.click()

    return


def OpenMaster(process_need: str):
    priemka_number = "48"
    process = FindProcess(process_need)

    FindImageAndClick("priemka_button.png")
    FindImageAndClick("List_master_button.png")

    pag.sleep(5)
    pag.moveTo(1819, 82, duration=0.5)
    pag.click()

    FindImageAndClick("choose_variants.png")

    pag.sleep(2)

    coordinate = (SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2)
    ClickButton(*coordinate)
    WaitProcess(process)

    pag.press("home")
    if FindItemInList("Список 1 этап"):
        pag.press("enter")

    ClickButton(1129, 124)

    pag.sleep(2.5)
    pag.press("delete")

    FindImageAndClick("add_button.png")
    FindImageAndClick("display_all.png")

    pag.sleep(1.5)
    FindImageAndClick("success_icon.png")

    pag.sleep(2.5)
    pag.press("home")

    FindItemInList(priemka_number)


def main():
    OpenMaster("1cv8c")


if __name__ == "__main__":
    main()
