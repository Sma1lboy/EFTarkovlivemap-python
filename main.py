"""This is temp doc str in python"""

import io
import json
import os
import threading
import time
import tkinter as tk
from pathlib import Path
from tkinter import ttk

import keyboard as kb
import sv_ttk
from PIL import Image, ImageTk
from selenium import webdriver
from selenium.webdriver.common.by import By

path = (
    Path(os.path.expanduser("~")) / "Documents" / "Escape from Tarkov" / "Screenshots"
)

statusLabel = None


def get_position_file():
    files = os.listdir(path)
    if len(files) == 0:
        return
    res = files[0]
    file = path / files[0]
    os.remove(file)
    return res


"""Delete useless element for screenshot, and make the marker more easy to see"""


def organize_element(driver: webdriver.Chrome):

    marker = driver.find_element(By.XPATH, '//*[@id="map"]/div')
    print("here is marker", marker)
    driver.execute_script("arguments[0].style.width='30px'", marker)
    driver.execute_script("arguments[0].style.height='30px'", marker)

    leftPane = driver.find_element(
        By.XPATH, "/html/body/div/div/div/div[2]/div/div/div[2]"
    )
    header = driver.find_element(By.XPATH, "/html/body/div/div/div/header")
    rightPane = driver.find_element(
        By.XPATH, "/html/body/div/div/div/div[2]/div/div/div[3]"
    )
    superHeader = driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]")
    footer = driver.find_element(By.XPATH, "/html/body/div/div/div/div[3]")
    topPane = driver.find_element(
        By.XPATH, '//*[@id="__nuxt"]/div/div/div[2]/div/div/div[1]'
    )
    elements = [header, leftPane, rightPane, superHeader, footer, topPane]

    for element in elements:
        if element:
            driver.execute_script("arguments[0].remove();", element)
    return


def fetchImage(map: str):
    global driver
    try:
        if "driver" not in globals():
            # options = webdriver.ChromeOptions()
            # options.add_argument("--headless")
            driver = webdriver.Chrome()
        if "driver" in globals() and driver.current_url != (
            "https://tarkov-market.com/maps/" + map
        ):
            driver.get("https://tarkov-market.com/maps/" + map)
            # get map ready
            button = driver.find_element(
                By.XPATH, '//*[@id="__nuxt"]/div/div/div[2]/div/div/div[1]/div/button'
            )
            time.sleep(0.5)
            button.click()
        inputForm = driver.find_element(
            By.XPATH, '//*[@id="__nuxt"]/div/div/div[2]/div/div/div[1]/div/input'
        )
        # Todo dev version, uncomment this later
        # inputForm.send_keys(get_position_file())
        organize_element(driver)
        res = driver.get_screenshot_as_png()
        time.sleep(0.5)  # wait for processing
        return res
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    finally:
        if driver != None:
            driver.quit()


def get_config():
    global _config, screenshotKey, isAutoRefresh, autoRefreshDuration, currMap
    with open("config.json", "r") as file:
        _config = json.loads(file.read())
    screenshotKey = _config["screenshotKey"].upper()
    isAutoRefresh = bool(_config["isAutoRefresh"])
    autoRefreshDuration = _config["autoRefreshDuration"]
    currMap = _config["currMap"]
    print("config load correctly...")


def keyboard_press_event(e: kb.KeyboardEvent):
    global isAutoRefresh, statusLabel, imageLabel, livemapWindow, currMap
    if e.name == "f5":
        isAutoRefresh = False
        statusLabel.config(text="Haven't start it yet")
        print("stop auto fresh for now")

    elif e.name == "f6":
        isAutoRefresh = True
        statusLabel.config(text="starting...")
        print("start auto refresh right now")
    elif e.name == screenshotKey.lower():
        image = get_image()
        livemapWindow.after(0, update_image_label, image)
        print("taking a picture")


def get_image():
    try:
        image = Image.open(io.BytesIO(fetchImage(currMap)))
        image = image.resize((300, 270))
        image = ImageTk.PhotoImage(image)
        return image
    except:
        print("cannot print image")
        return None


def keyboard_listener():
    global autoRefreshDuration
    kb.on_press(keyboard_press_event)
    while True:
        if isAutoRefresh:
            image = get_image()
            update_image_label(image)
        time.sleep(autoRefreshDuration)


def setup_kb_thread():
    kb_thread = threading.Thread(target=keyboard_listener)
    kb_thread.daemon = True
    kb_thread.start()
    return kb_thread


def update_image_label(image):
    if image == None:
        return
    global imageLabel
    imageLabel.config(image=image)
    imageLabel.image = image


def create_livemap_window():
    global livemapWindow, imageLabel
    livemapWindow = tk.Toplevel()
    livemapWindow.attributes("-topmost", True)
    # livemapWindow.resizable((False, False))
    livemapWindow.geometry("+0+0")
    imageLabel = tk.Label(master=livemapWindow)
    imageLabel.pack()


def create_main_window():
    window = tk.Tk()
    window.title("EFTarkov Livemap")
    # introductionText = tk.Label(text="")

    currKeyFrame = tk.Frame(master=window)
    currKeyFrame.grid()
    tk.Label(
        master=currKeyFrame,
        text="Welcome to Tarkov Live Map, the first version of this open source software.\nUse F5 to stop the program, F6 to start livemap,\n or you can use the custom screenshot button to update the map location when you want.",
        justify=tk.LEFT,
    ).grid(sticky="w", row=0, column=0)
    tk.Label(master=currKeyFrame, text="the current key you are using: ").grid(
        sticky="w", row=1, column=0
    )
    entry = tk.Entry(master=currKeyFrame)
    entry.insert(0, screenshotKey)
    entry.grid(row=1, column=1)

    tk.Label(master=currKeyFrame, text="current map choice: ").grid(
        sticky="w", row=2, column=0
    )
    mapCombobox = ttk.Combobox(master=currKeyFrame, state="readonly")
    map_opts_dict = {
        "Factory": "factory",
        "Ground Zero": "ground-zero",
        "Customs": "customs",
        "Interchange": "interchange",
        "Woods": "woods",
        "Shoreline": "shoreline",
        "Reserve": "reserve",
        "Lighthouse": "lighthouse",
        "Street of Tarkov": "streets",
        "The Lab": "lab",
    }
    map_opts = [key for key, _ in map_opts_dict.items()]
    mapCombobox["values"] = map_opts
    mapCombobox.current(0)  # setup default map
    mapCombobox.grid(row=2, column=1)

    def map_selected_event(e):
        global currMap
        currMap = map_opts_dict[mapCombobox.get()]
        print("current map is ", currMap)

    mapCombobox.bind("<<ComboboxSelected>>", map_selected_event)
    tk.Label(text="current status: ").grid(sticky="w", row=3, column=0)
    global statusLabel
    statusLabel = tk.Label(text="Not start")
    statusLabel.grid(sticky="w", row=3, column=1)
    return window


if __name__ == "__main__":
    global isAutoRefresh, screenshotKey, currMap, driver
    try:
        # init config
        get_config()
        # craete main window
        window = create_main_window()

        create_livemap_window()
        setup_kb_thread()

        sv_ttk.set_theme("dark")
        window.mainloop()
    finally:
        if "driver" in globals():
            driver.close()
