from os import system
import json
try:
    import requests
except:
    system('pip install requests')
    system('python3 -m pip install requests')
    import requests
try:
    from selenium.webdriver.common.by import By
except:
    system('pip install selenium')
    system('python3 -m pip install selenium')
    from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
try:
    from webdriver_manager.chrome import ChromeDriverManager
except:
    system('pip install webdriver_manager')
    system('python3 -m pip install webdriver_manager')
    from webdriver_manager.chrome import ChromeDriverManager
try:
    from selenium_authenticated_proxy import SeleniumAuthenticatedProxy
except:
    system('pip install selenium_authenticated_proxy')
    system('python3 -m pip install selenium_authenticated_proxy')
    from selenium_authenticated_proxy import SeleniumAuthenticatedProxy
try:
    from fake_useragent import UserAgent
except:
    system('pip install fake_useragent')
    system('python3 -m pip install fake_useragent')
    from fake_useragent import UserAgent

def get_cookies_useragent(site_url):
    count = 0
    while True:
        count += 1
        ua = UserAgent()
        usr_agent = ua.firefox
        options = webdriver.ChromeOptions()
        options.add_argument(f"user-agent={usr_agent}")
        options.add_argument("--window-size=375,667")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless=new")
        PROXY_HOST = 'rp.proxyscrape.com'  # rotating proxy or host
        PROXY_PORT = 6060 # port
        PROXY_USER = 'x5x6d54u9x3pgr7' # username
        PROXY_PASS = 'vel5vfhtwpo8yq4' # password

        proxy_helper = SeleniumAuthenticatedProxy(
            proxy_url=f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}")

        proxy_helper.enrich_chrome_options(options)

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
        
        driver.get(site_url)
        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, f'(//ol[@data-results-grid-container=""]/li)[1]')))
            break
        except:
            driver.save_screenshot(f'err-{count}.png')
            driver.delete_all_cookies()
            driver.quit()
    
    page_source = driver.page_source

    with open('web_page_se.html', 'w', encoding='utf-8') as file:
        file.write(page_source)
    return driver.get_cookies(), usr_agent

cookies, usr_agent = get_cookies_useragent('https://www.etsy.com/de-en/search?q=mug&ref=search_bar')

cookies_str = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': usr_agent,
    'Cookie': cookies_str
})

response = requests.get('https://www.etsy.com/de-en/search?q=mug&ref=search_bar', headers=headers)

with open('web_page_re.html', 'w', encoding='utf-8') as file:
    file.write(response.content.decode('utf-8'))

with open('headers.json', 'w', encoding='utf-8') as file:
    json.dump(dict(headers), file, ensure_ascii=False, indent=4)


# 'https://www.etsy.com/de-en/search?q=mug&ref=search_bar'
# nextPage_xpath = '//span[text()="Next"]/../../a[contains(@href,"pagination")]'