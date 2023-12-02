import re
import csv
import pandas as pd
from requests import Session
from bs4 import BeautifulSoup
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

url_address = {}

ua = UserAgent()
usr_agent = ua.random
chrome_options = Options()
chrome_options.add_argument(f"user-agent={usr_agent}")
chrome_options.add_argument("--window-size=375,667")
chrome_options.add_argument("--lang=en")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def get_address(driver, location_url):
    if location_url in url_address.keys():
        return url_address[location_url]
    else:
        while True:
            try:
                try:
                    driver.get(location_url)
                except:
                    driver.save_screenshot('screenshot.png')
                    raise Exception('failed to load page')
                try:
                    address = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                            (By.XPATH, '//img[contains(@src,"place") and contains(@src,"icon")]/../../..//*[text()!=""]'))).text
                except:
                    address = ''
                finally:
                    driver.get('data:,')
                    driver.delete_all_cookies()
                    url_address[location_url] = address
                break
            except:
                try:
                    driver.quit()
                except:
                    ...
                del driver
                ua = UserAgent()
                usr_agent = ua.random
                chrome_options = Options()
                chrome_options.add_argument(f"user-agent={usr_agent}")
                chrome_options.add_argument("--window-size=375,667")
                chrome_options.add_argument("--lang=en")
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-gpu")

                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        return address

address = get_address(driver, 'https://www.google.com/maps/search/?api=1&query=Koncerten%20-%20Ollerup%20Efterskole%20Sang%20%26%20Musik')
print(address)
