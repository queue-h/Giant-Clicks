from playwright.sync_api import sync_playwright
import random
import time

GIANT_HOME = "https://giantfood.com/"
USER_AGENTS = ["Mozilla/5.0 (Android 15; Mobile; rv:136.0) Gecko/136.0 Firefox/136.0",
               "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/136.0 Mobile/15E148 Safari/605.1.15",
               "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
               "Mozilla/5.0 (X11; Linux i686; rv:128.0) Gecko/20100101 Firefox/128.0",
               "Mozilla/5.0 (X11; Linux i686; rv:136.0) Gecko/20100101 Firefox/136.0",
               "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:151.0) Gecko/20100101 Firefox/151.0"]

with sync_playwright() as pw:
    # go to browser
    browser = pw.firefox.launch(headless=False)
    # add random proxies
    context = browser.new_context(user_agent=random.choice(USER_AGENTS))

    # inject JavaScript to disable the webdriver flag
    context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
        """)

    page = context.new_page()
    page.goto(GIANT_HOME)
    print(page.title())

    # go to sign-in
    signin_button = page.get_by_role("button", name="Sign in")
    signin_button.click()
    page.screenshot(path="sign-in.png")


def human_click(element):
    box = element.bounding_box()
    if box:
        # move mouse to a random point within the element
        x = box["x"] + box["width"] * random.random()
        y = box["y"] + box["height"] * random.random()
        # smooth mouse movement
        page.mouse.move(x, y, steps=random.randint(5, 15))  # Smooth movement
        page.mouse.click(x, y)
        # random delay after click
        time.sleep(random.uniform(0.5, 1.5))


