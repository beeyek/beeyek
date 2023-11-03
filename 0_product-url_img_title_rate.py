from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
from time import sleep
from selenium.webdriver.common.keys import Keys
import csv
from amazoncaptcha import AmazonCaptcha
from pathlib import Path
current_directory = Path().absolute()
data_directory  = current_directory.joinpath("product-url_img_title_rate")



site_url = 'https://www.amazon.com/'

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

driver.get(site_url)
driver.refresh()

keyword = 'protein shaker'
data_list = []
def solve_captcha():
    captcha_img_url = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, f'//img[contains(@src,"Captcha")]'))).get_attribute('src')
    captcha = AmazonCaptcha.fromlink(captcha_img_url)
    solution = captcha.solve()
    cap_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, f'//input[@id="captchacharacters"]')))
    cap_input.send_keys(solution)
    cap_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, f'//button[@type="submit"]')))
    cap_btn.click()

while True:
    try:
        solve_captcha()
    except:
        break

input('--')

search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//input[@id="twotabsearchtextbox"]')))
search_submit_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//input[@id="nav-search-submit-button"]')))

search_box.send_keys(keyword)
search_submit_btn.click()


def load_products():
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//body'))).send_keys(Keys.CONTROL+Keys.END)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '(//a[contains(@aria-label,"Go to next page")]/../../../..)[contains(@data-cel-widget,"search_result_")]')))
    except:
        ...

load_products()

last_page = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '(//*[contains(@class,"s-pagination-item")])[last()-1]')))
print(last_page.text)
count = 0
for i in range(int(last_page.text)):
    print('count',count)
    all_products = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
        (By.XPATH, '//div[@data-component-type="s-search-result"]')))
    print(len(all_products))
    
    load_products()

    all_products = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
        (By.XPATH, '//div[@data-component-type="s-search-result"]')))
    print(len(all_products))
    
    for index in range(len(all_products)):
        indexx = index + 1

        product_image_url = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, f'//div[@data-component-type="s-search-result"][{indexx}]//img[@data-image-latency="s-product-image"]'))).get_attribute('src')
        
        product_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, f'//div[@data-component-type="s-search-result"][{indexx}]//div[contains(@class,"s-title-instructions-style")]/h2'))).text
        
        try:
            product_rate = driver.find_element(By.XPATH,f'//div[@data-component-type="s-search-result"][{indexx}]//span[contains(@aria-label,"star")]').get_attribute('aria-label')
        except:
            product_rate = '-'

        product_url = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, f'//div[@data-component-type="s-search-result"][{indexx}]//div[contains(@class,"s-title-instructions-style")]/h2/a'))).get_attribute('href')
        
        data1 = [product_url,product_image_url,product_title,product_rate]
        data_list.append(data1)
    
    try:
        next_page_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, '//a[contains(@aria-label,"Go to next page")]')))
    except:
        break
    try:
        next_page_btn.click()
    except:
        try:
            next_page_btn = driver.find_element(By.XPATH, '//a[contains(@aria-label,"Go to next page")]')
            next_page_btn.click()
        except:
            input('error 111')
    count+=1

data_json = {
    "product_data":data_list
}
with open(data_directory.joinpath(f'product_url({keyword}).json'),'w', encoding='utf-8') as file:
    json.dump(data_json, file)
print("--------------\nend\n---------------")