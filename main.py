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

path = Path(os.path.expanduser("~")) / 'Documents' / 'Escape from Tarkov' / 'Screenshots'

def getFile():
    files = os.listdir(path)
    if len(files) == 0:
        return;
    res = files[0]
    file = path + files[0]
    os.remove(file)
    return res

if __name__ == "__main__":
    print("init proj")