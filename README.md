## Selenium-recaptcha-solver

This package is used to solve recaptcha challenges when 
using a Selenium web driver for web automation tasks.

It supports single-step and multi-step audio solving for ReCAPTCHA audio challenges.

## Requirements 

Python 3.7+

Main dependencies:
  <ul>
    <li>SpeechRecognition python package to transcribe speech</li>
    <li>Pydub for file conversions</li>
</ul>

## Installation

```bash
python -m pip install selenium-recaptcha-solver
```

## Usage

```python
from selenium_recaptcha_solver import API
from selenium import webdriver

# Example driver, the API works for any browser
driver = webdriver.Chrome()

# Create API object and bind it to your webdriver
api_client = API(driver=driver)

# Fetch random web page
driver.get('https://foo.bar.com')

# Get example iframe web element
iframe = driver.find_element(
    by='foo', 
    value='bar',
)

# Solve Captcha using API (Usually used for Captcha challenges or invisible ReCaptchaV2)
api_client.solve_recaptcha_v2(iframe=iframe)

# Or solve a Captcha V2 visible (The one where you have to click a checkbox - If a challenge pops up after the click it's automatically resolved)
api_client.click_recaptcha_v2(iframe=iframe)

# Write the rest of your operations to do after solving the Captcha
```

## Demonstration
[![Image from Gyazo](https://i.gyazo.com/858ceb5df9f43f6aafadf69e233cd2d1.gif)](https://gyazo.com/858ceb5df9f43f6aafadf69e233cd2d1)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
