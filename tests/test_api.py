from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium_recaptcha_solver.api import API
from selenium import webdriver
import pytest


options = webdriver.ChromeOptions()

options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")

options.add_argument('--no-sandbox')
options.add_argument("--disable-extensions")

service = Service(ChromeDriverManager().install())

test_driver = webdriver.Chrome(options=options, service=service)

solver = API(driver=test_driver)


def test_solver():
    try:
        test_driver.get('https://www.google.com/recaptcha/api2/demo')

        element = ('xpath', '//iframe[@title="reCAPTCHA"]')

        WebDriverWait(test_driver, 5).until(ec.visibility_of_element_located(element))

        recaptcha_iframe = test_driver.find_element(*element)

        solver.click_recaptcha_v2(iframe=recaptcha_iframe)

    except Exception:
        pytest.fail('Failed to automatically resolve ReCAPTCHA.')
