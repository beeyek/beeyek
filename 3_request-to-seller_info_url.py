import csv
from pathlib import Path
import json
from pathlib import Path
from lxml import html
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from amazoncaptcha import AmazonCaptcha
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

keyword = 'blender bottle'

current_directory = Path().absolute()
result_directory = current_directory.joinpath("excavating_information")
data_seller_directory = current_directory.joinpath("request-to-seller_info_url")

seller_info_urls = []

with open(result_directory.joinpath(f'result_product({keyword}).csv'), mode='r', encoding='utf-8', newline='') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        seller_info_url = row[-1]  
        seller_info_urls.append(seller_info_url)


ua = UserAgent()
usr_agent = ua.random
print(usr_agent)

options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={usr_agent}")
options.add_argument("--start-maximized")

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

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
driver.get('https://www.amazon.com/errors/validateCaptcha')

while True:
    try:
        solve_captcha()
    except:
        break

input('--')

request_info = driver.requests[-1]
HEADERS = dict(request_info.headers)
cookies = driver.get_cookies()
cookie_str = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
if "Cookie" in HEADERS.keys():
    HEADERS.pop('Cookie', None)
if "cookie" in HEADERS.keys():
    HEADERS.pop('cookie', None)
HEADERS['Cookie'] = cookie_str
keys_to_remove = []
for key in HEADERS.keys():
    if key not in ["user-agent", "accept", "accept-encoding", "Cookie"]:
        keys_to_remove.append(key)

for key in keys_to_remove:
    del HEADERS[key]
HEADERS['Connection'] = 'keep-alive'
HEADERS["Upgrade-Insecure-Requests"] = "1"
HEADERS["Accept-Language"] = "en-US, en;q=0.5"

driver.get('https://stackoverflow.com')

print('----------\n',HEADERS,'\n-------------')

for index in range(len(seller_info_urls)):
    if seller_info_urls[index] == '-':
        continue
    print(seller_info_urls[index])
    while True:
        print('----------\n',HEADERS,'\n-------------')
        print('----------\n',seller_info_urls[index],'\n-------------')
        res = requests.get(seller_info_urls[index], headers=HEADERS)
        tree = html.fromstring(res.content)
        cookies_from_requests = res.cookies.get_dict()

        captcha = tree.xpath('//input[@id="captchacharacters"]')
        error_500_503 = tree.xpath('//img[contains(@src,"error") and contains(@src,"500_503")]')

        if captcha or error_500_503:
            if captcha:
                print("----------\ncaptcha found\n----------")
            if error_500_503:
                print("----------\nerror_500_503 found\n----------")
            for cookie_name, cookie_value in cookies_from_requests.items():
                driver.add_cookie({'name': cookie_name, 'value': cookie_value})
            driver.get(seller_info_urls[index])
            captcha_solved_count = 0
            while True:
                try:
                    solve_captcha()
                    captcha_solved_count += 1
                except:
                    if captcha_solved_count == 0:
                        driver.get('https://www.amazon.com/errors/validateCaptcha')
                        while True:
                            try:
                                solve_captcha()
                            except:
                                break
                    request_info = driver.requests[-1]
                    HEADERS = dict(request_info.headers)
                    cookies = driver.get_cookies()
                    cookie_str = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
                    if "Cookie" in HEADERS.keys():
                        HEADERS.pop('Cookie', None)
                    if "cookie" in HEADERS.keys():
                        HEADERS.pop('cookie', None)
                    HEADERS['Cookie'] = cookie_str
                    keys_to_remove = []
                    for key in HEADERS.keys():
                        if key not in ["user-agent", "accept", "accept-encoding", "Cookie"]:
                            keys_to_remove.append(key)

                    for key in keys_to_remove:
                        del HEADERS[key]
                    HEADERS['Connection'] = 'keep-alive'
                    HEADERS["Upgrade-Insecure-Requests"] = "1"
                    HEADERS["Accept-Language"] = "en-US, en;q=0.5"


                    driver.get('https://stackoverflow.com')

                    break
            downloaded = False
        elif res.status_code != 200:
            print(res.status_code)
            downloaded = False
        else:
            with open(data_seller_directory.joinpath(f'{index}_seller_html({keyword}).html'), 'w', encoding='utf-8') as file:
                file.write(res.content.decode('utf-8'))
            downloaded = True
        
        if downloaded:
            break

input("--------------\nend\n---------------")


