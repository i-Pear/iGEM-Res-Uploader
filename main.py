import time
import request
import pymysql
import datetime
import pyperclip
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import support, ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions

if __name__ == '__main__':

    with open(r'D:\res.txt') as file:
        resList = file.readlines()

    for i in range(len(resList)):
        resList[i] = resList[i][:-1]

    d = DesiredCapabilities.CHROME
    d['loggingPrefs'] = {'browser': 'ALL', 'performance': 'ALL'}
    options = webdriver.ChromeOptions()
    options.add_experimental_option('perfLoggingPrefs', {
        'enableNetwork': True,
        'enablePage': False,
    })

    browser = webdriver.Chrome(desired_capabilities=d)

    browser.get("https://2019.igem.org/wiki/index.php?title=Special:Upload&wpDestFile=123.html")
    print('Press Enter')
    input()
    count = 0

    for res in resList:
        browser.get("https://2019.igem.org/wiki/index.php?title=Special:Upload&wpDestFile=T--NEU_CHINA--" + res)
        WebDriverWait(browser, 10).until(lambda x: len(x.find_elements_by_id("wpUploadFile")))
        browser.find_element_by_id("wpUploadFile").send_keys(r'G:\igem_page2\source\ '[:-1] + res)
        browser.find_element_by_name("wpUpload").click()
        WebDriverWait(browser, 10).until(lambda x: len(x.find_elements_by_link_text("Original file"))
                                                   + len(x.find_elements_by_link_text("T--NEU_CHINA--" + res))
                                                   + len(x.find_elements_by_name("wpUploadIgnoreWarning")))

        if len(browser.find_elements_by_name("wpUploadIgnoreWarning")) > 0:
            browser.find_element_by_name("wpUploadIgnoreWarning").click()
            WebDriverWait(browser, 10).until(lambda x: len(x.find_elements_by_link_text("Original file"))
                                                       + len(x.find_elements_by_link_text("T--NEU_CHINA--" + res)))

        if len(browser.find_elements_by_link_text("Original file")) > 0:
            href = browser.find_element_by_link_text("Original file").get_attribute("href")
        else:
            href = browser.find_element_by_link_text("T--NEU_CHINA--" + res).get_attribute("href")
        count += 1
        print("uploaded", count, " :", href)

    input()
