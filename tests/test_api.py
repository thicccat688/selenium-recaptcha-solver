from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium_recaptcha_solver.api import API
from selenium import webdriver
import pytest


test_driver = webdriver.Chrome()

options = webdriver.ChromeOptions()

# options.headless = True

service = Service(ChromeDriverManager().install())

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
