from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc
import pytest

from selenium_recaptcha_solver.api import API


test_ua = 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'

options = uc.ChromeOptions()

options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")

options.add_argument(f'--user-agent={test_ua}')
options.add_argument('--incognito')

options.add_argument('--no-sandbox')
options.add_argument("--disable-extensions")

test_driver = uc.Chrome(options=options)

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
