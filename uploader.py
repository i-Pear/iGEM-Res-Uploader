import os
import sys
import time
import request
import pymysql
import datetime
import pyperclip
import traceback
import win32clipboard as w
import win32api
import win32con
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import support, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions


# 用于设置剪切板内容
def setText(aString):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
    w.CloseClipboard()


# 键盘按键映射字典
VK_CODE = {
    'enter': 0x0D,
    'ctrl': 0x11,
    'v': 0x56,
    'a': 0x41,
    'del': 0x08
}


# 键盘键按下
def keyDown(keyName):
    win32api.keybd_event(VK_CODE[keyName], 0, 0, 0)


# 键盘键抬起
def keyUp(keyName):
    win32api.keybd_event(VK_CODE[keyName], 0, win32con.KEYEVENTF_KEYUP, 0)


def combinKey(keys):
    for i in range(len(keys)):
        keyDown(keys[i])
    for i in range(0, len(keys))[::-1]:
        keyDown(keys[i])


if __name__ == '__main__':

    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'browser': 'ALL', 'performance': 'ALL'}
    options = webdriver.ChromeOptions()
    options.add_experimental_option('perfLoggingPrefs', {
        'enableNetwork': True,
        'enablePage': False,
    })

    browser = webdriver.Chrome(desired_capabilities=d)

    browser.get("https://2019.igem.org/wiki/index.php?title=Special:Upload&wpDestFile=123.html")
    print("Press enter")
    input()
    time.sleep(2)

    parPath = "G:\igem_page2"

    for root, dirs, files in os.walk(parPath):
        for file in files:
            if not (file.endswith("-css") or file.endswith(".html") or file.endswith("-js")):
                continue

            print("Uploading " + file)
            path = os.path.join(root, file)
            webPathSeg = (path[len(parPath):]).replace('\\', '/')
            with open(path, encoding='utf-8') as filex:
                lines = filex.readlines()

            text = ""
            for i in range(len(lines)):
                text = text + lines[i]  # Combine

            webPath = "https://2019.igem.org/wiki/index.php?title=Team:NEU_CHINA" + webPathSeg + "&action=edit"
            browser.get(webPath)
            WebDriverWait(browser, 20).until(lambda x: len(x.find_elements_by_id("wpTextbox1")))

            setText(text)
            browser.find_element_by_id("wpTextbox1").click()
            combinKey(['ctrl', 'a'])
            combinKey(['del'])
            combinKey(['ctrl', 'v'])
            time.sleep(1)

            browser.find_element_by_name("wpSave").click()
            time.sleep(1)
