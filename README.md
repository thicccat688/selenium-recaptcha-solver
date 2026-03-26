## Selenium-recaptcha-solver

You can use this package to solve ReCAPTCHA challenges with selenium.

It supports single-step and multi-step audio solving for ReCAPTCHA V2 with >90% success rate.

Please use this package responsibly and for non-exploitative ends.

Notice: This project is no longer being maintained.

## Requirements 

Python 3.7+

Main dependencies:
<ul>
    <li>SpeechRecognition python package to transcribe speech</li>
    <li>Pydub for file conversions</li>
    <li>Requests for HTTP requests</li>
    <li>Selenium for web driver </li>
</ul>

If you're getting an error related to FFmpeg not being installed or in your PATH, get it here: https://ffmpeg.org/download.html

If the error persists, make sure FFmpeg is properly installed for your OS and in your PATH.

<!-- 
=============================================================
⚠️ PROPOSAL FOR ADVERTISING / SPONSORSHIP ⚠️

Hi! I'd like to place this advertisement in your repository.
If you're interested in sponsorship or advertising, please contact me:

📱 Telegram: @keropo
🔗 LinkedIn: https://www.linkedin.com/in/kirill-ponomarev-k/

This is just a proposal — feel free to reject or modify!
=============================================================
-->

<!-- AD -->
---
## Sponsors

✅ CapMonster.Cloud — Fast, Reliable CAPTCHA Solving for Automation & Scraping

[![CapMonster Cloud](https://help.zennolab.com/upload/u/02/020538b7c128.png)](https://capmonster.cloud/en/?utm_source=github&utm_campaign=thicccat688_selenium-recaptcha-solver)

If you are tired of wasting time solving endless CAPTCHAs during scraping, automation, or testing — we’ve got a solution for you.  
Meet CapMonster.Cloud — the AI-powered CAPTCHA solving service trusted by thousands of users worldwide. 🚀

--

🔥 **Why users love CapMonster.Cloud**
  
💡 Very high success rates (up to 99%)  
⚡ Super fast solving times  
💲 Affordable transparent pricing (pay per 1,000 CAPTCHAs)  
🔌 Easy integration via API + browser extensions  
⭐ Excellent reviews on TrustPilot, SourceForge, SaaSHub, AlternativeTo

--

🔗 **Useful Links**

💲 [Pricing & Supported CAPTCHA Types (25+ types supported)](https://capmonster.cloud/en?utm_source=github&utm_campaign=thicccat688_selenium-recaptcha-solver#new-plans)  
📘 [API Documentation](https://docs.capmonster.cloud/?utm_source=github&utm_campaign=thicccat688_selenium-recaptcha-solver)  
💡 Main Website → [capmonster.cloud](https://capmonster.cloud/en/?utm_source=github&utm_campaign=thicccat688_selenium-recaptcha-solver)  
⭐ Reviews → [TrustPilot](https://www.trustpilot.com/review/capmonster.cloud)

---
<!-- /AD -->

## Installation

```bash
python -m pip install selenium-recaptcha-solver
```

## Usage example with ReCAPTCHA demo site

```python
from selenium_recaptcha_solver import RecaptchaSolver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


test_ua = 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'

options = Options()

options.add_argument("--headless")  # Remove this if you want to see the browser (Headless makes the chromedriver not have a GUI)
options.add_argument("--window-size=1920,1080")

options.add_argument(f'--user-agent={test_ua}')

options.add_argument('--no-sandbox')
options.add_argument("--disable-extensions")

test_driver = webdriver.Chrome(options=options)

solver = RecaptchaSolver(driver=test_driver)

test_driver.get('https://www.google.com/recaptcha/api2/demo')

recaptcha_iframe = test_driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')

solver.click_recaptcha_v2(iframe=recaptcha_iframe)
```

You can check a detailed use case in the tests folder of this project (Its execution is shown below in the demonstration chapter).

## Demonstration
[![Image from Gyazo](https://i.gyazo.com/858ceb5df9f43f6aafadf69e233cd2d1.gif)](https://gyazo.com/858ceb5df9f43f6aafadf69e233cd2d1)

## Avoiding detection

To decrease your chances of ReCAPTCHA detecting automated queries, try the following:
- Use a custom user-agent header (Make sure it's not a headless user-agent!)
- Use a hard-to-detect web driver 
- Use proxies to avoid IP blacklisting

An example of a good user-agent: Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36

An example of a bad user-agent: are Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/92.0.4512.0 Safari/537.36

Note the last part of the user-agent; the headless specification is usually there.

## Questions
If the documentation hasn't covered something, or you have questions about how to use the package or how it works, please reach out.
