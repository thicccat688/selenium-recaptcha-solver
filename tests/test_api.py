from selenium_recaptcha_solver import RecaptchaSolver, StandardDelayConfig
from selenium.webdriver.common.by import By
import undetected_chromedriver as webdriver
import pytest


test_ua = 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'

options = webdriver.ChromeOptions()

options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")

options.add_argument(f'--user-agent={test_ua}')
options.add_argument('--incognito')

options.add_argument('--no-sandbox')
options.add_argument("--disable-extensions")

test_driver = webdriver.Chrome(options=options)

solver = RecaptchaSolver(driver=test_driver, delay_config=StandardDelayConfig())


def test_solver():
    try:
        test_driver.get('https://www.google.com/recaptcha/api2/demo')

        recaptcha_iframe = test_driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')

        solver.click_recaptcha_v2(iframe=recaptcha_iframe)

    except Exception:
        pytest.fail('Failed to automatically resolve ReCAPTCHA.')
