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

    ofs = open(r'D:\out.txt', "w")
    browser.get("https://2019.igem.org/wiki/index.php?title=Special:Upload&wpDestFile=123.html")

    print("Press enter after you login in")
    i = input()

    for res in resList:
        browser.get("https://2019.igem.org/File:" + res)
        herf = "NULL!"
        try:
            WebDriverWait(browser, 10).until(lambda x: len(x.find_elements_by_link_text("Original file"))
                                                       + len(x.find_elements_by_link_text(res)))
            if len(browser.find_elements_by_link_text("Original file")) > 0:
                href = browser.find_element_by_link_text("Original file").get_attribute("href")
            else:
                href = browser.find_element_by_link_text(res).get_attribute("href")
        except expected_conditions:
            print("", end='')

        ofs.write(res + "\t" + href + "\n")
        print(res)

    ofs.close()
