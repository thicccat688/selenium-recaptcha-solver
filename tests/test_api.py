from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium_recaptcha_solver import RecaptchaSolver, StandardDelayConfig
from selenium_stealth import stealth
from selenium import webdriver
import pytest


test_ua = 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'

options = webdriver.ChromeOptions()

# options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")

options.add_argument(f'--user-agent={test_ua}')
options.add_argument('--incognito')

options.add_argument('--no-sandbox')
options.add_argument("--disable-extensions")


test_driver = webdriver.Chrome(options=options)


stealth(
    test_driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)


solver = RecaptchaSolver(driver=test_driver, delay_config=StandardDelayConfig())


def test_solver():
    try:
        test_driver.get('https://www.google.com/recaptcha/api2/demo')

        element = ('xpath', '//iframe[@title="reCAPTCHA"]')

        WebDriverWait(test_driver, 5).until(ec.visibility_of_element_located(element))

        recaptcha_iframe = test_driver.find_element(*element)

        solver.click_recaptcha_v2(iframe=recaptcha_iframe)

    except Exception:
        pytest.fail('Failed to automatically resolve ReCAPTCHA.')
