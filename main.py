from selenium import  webdriver
from selenium.webdriver.common.by import By

import requests
import keyboard as kb
import time
import os
from pathlib import Path

import json
import traceback
import atexit
import tkinter as tk

path = Path(os.path.expanduser("~")) / 'Documents' / 'Escape from Tarkov' / 'Screenshots'

def get_position_file():
    files = os.listdir(path)
    if len(files) == 0:
        return;
    res = files[0]
    file = path / files[0]
    os.remove(file)
    return res

def delete_useless_element(driver):
    leftPane = driver.find_element(By.XPATH, "/html/body/div/div/div/div[2]/div/div/div[2]")
    header = driver.find_element    (By.XPATH,"/html/body/div/div/div/header")
    rightPane = driver.find_element(By.XPATH,"/html/body/div/div/div/div[2]/div/div/div[3]")
    superHeader = driver.find_element(By.XPATH,"/html/body/div/div/div/div[1]")
    footer = driver.find_element(By.XPATH, "/html/body/div/div/div/div[3]")
    topPane = driver.find_element(By.XPATH, "//*[@id=\"__nuxt\"]/div/div/div[2]/div/div/div[1]")
    elements = [header, leftPane, rightPane, superHeader, footer, topPane]

    for element in elements:
        if element:
            driver.execute_script("arguments[0].remove();", element)
    return

def fetchImage(map:str):
    # options = webdriver.ChromeOptions();
    # options.add_argument("--headless")
    # driver = webdriver.Chrome(options)
    driver = webdriver.Chrome()
    driver.get("https://tarkov-market.com/maps/" + map)

    # get map ready
    button = driver.find_element(By.XPATH, "//*[@id=\"__nuxt\"]/div/div/div[2]/div/div/div[1]/div/button")
    time.sleep(1)
    button.click()
    input = driver.find_element(By.XPATH, "//*[@id=\"__nuxt\"]/div/div/div[2]/div/div/div[1]/div/input")
    # input.send_keys(get_position_file())

    delete_useless_element(driver)
    res = driver.get_screenshot_as_png()
    driver.quit()
    return res;

def getConfig():
    global _config;    
    with open("config.json", 'r') as file:
        _config = json.loads(file.read())

    print(_config["isAutoRefresh"])

def loopPressKeyboard():
    def onHotKeyPress():

        return
    
    kb.add_hotkey("F9", print, args=('triggered', 'hotkey'))

if __name__ == "__main__":
    # window = tk.Tk("projectpay")
    loopPressKeyboard()
    kb.send("F9")
    kb.wait()