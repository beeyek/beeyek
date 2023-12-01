from playwright.sync_api import sync_playwright

def run_playwright():
    PROXY_HOST = 'rp.proxyscrape.com'
    PROXY_PORT = 6060
    PROXY_USER = 'x5x6d54u9x3pgr7'
    PROXY_PASS = 'vel5vfhtwpo8yq4'
    proxy_url=f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
    proxy = {
        'server': proxy_url,
        'username': PROXY_USER,
        'password': PROXY_PASS,
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, proxy=proxy)
        context = browser.new_context()
        page = context.new_page()

        page.goto('https://api.ipify.org/')
        print(page.title())
        with open('1.html', 'w') as file:
            file.write(page.content())

        browser.close()

if __name__ == "__main__":
    run_playwright()
