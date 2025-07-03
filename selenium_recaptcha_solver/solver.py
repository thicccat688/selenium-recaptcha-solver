from selenium_recaptcha_solver.exceptions import RecaptchaException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from pydub import AudioSegment
from typing import Optional
import speech_recognition as sr
import tempfile
import requests
import random
import uuid
import time
import os

from .delay_config import DelayConfig, StandardDelayConfig
from .services import Service, GoogleService


DEFAULT_SERVICE: Service = GoogleService()


class RecaptchaSolver:
    def __init__(
            self,
            driver: WebDriver,
            service: Service = DEFAULT_SERVICE,
            service_language: str = 'en-US',
            delay_config: Optional[DelayConfig] = None,
    ):
        """
        :param driver: Selenium web driver to use to solve the captcha
        :param service: service to use for speech recognition (defaults to ``GoogleService``).
            See the ``services`` module for available services.
        :param service_language: Language to use when recognizing speech to solve reCAPTCHA challenge (en-US by default for American English recognition)
        :param delay_config: if set, use the given configuration for delays between UI interactions.
            See :class:`DelayConfig`, and also :class:`StandardDelayConfig`, which provides a standard implementation that should work in many cases.
        """

        self._driver = driver
        self._service = service
        self._delay_config = delay_config
        self._language = service_language

        # Initialise speech recognition API object
        self._recognizer = sr.Recognizer()

    def click_recaptcha_v2(self, iframe: WebElement, by_selector: Optional[str] = None) -> None:
        """
        Click the "I'm not a robot" checkbox and then solve a reCAPTCHA v2 challenge.

        Call this method directly on web pages with an "I'm not a robot" checkbox. See <https://developers.google.com/recaptcha/docs/versions> for details of how this works.

        :param iframe: web element for inline frame of reCAPTCHA to solve
        :param by_selector: By selector to use to find the iframe, if ``iframe`` is a string
        :raises selenium.common.exceptions.TimeoutException: if a timeout occurred while waiting
        """

        if isinstance(iframe, str):
            WebDriverWait(self._driver, 10).until(
                ec.frame_to_be_available_and_switch_to_it((by_selector, iframe)))

        else:
            self._driver.switch_to.frame(iframe)

        checkbox = self._wait_for_element(
            by='id',
            locator='recaptcha-anchor',
            timeout=10,
        )

        self._js_click(checkbox)

        if checkbox.get_attribute('aria-checked') == 'true':
            return

        if self._delay_config:
            self._delay_config.delay_after_click_checkbox()

        self._driver.switch_to.parent_frame()

        captcha_challenge = self._wait_for_element(
            by=By.XPATH,
            locator='//iframe[contains(@src, "recaptcha") and contains(@src, "bframe")]',
            timeout=5,
        )

        self.solve_recaptcha_v2_challenge(iframe=captcha_challenge)

    def solve_recaptcha_v2_challenge(self, iframe: WebElement) -> None:
        """
        Solve a reCAPTCHA v2 challenge that has already appeared.

        Call this method directly on web pages with the "invisible reCAPTCHA" badge. See <https://developers.google.com/recaptcha/docs/versions> for details of how this works.

        :param iframe: Web element for inline frame of reCAPTCHA to solve
        :raises selenium.common.exceptions.TimeoutException: if a timeout occurred while waiting
        """

        self._driver.switch_to.frame(iframe)

        # If the captcha image audio is available, locate it. Otherwise, skip to the next line of code.

        try:
            self._wait_for_element(
                by=By.XPATH,
                locator='//*[@id="recaptcha-audio-button"]',
                timeout=1,
            ).click()

        except TimeoutException:
            pass

        self._solve_audio_challenge(self._language)

        # Locate verify button and click it via JavaScript
        verify_button = self._wait_for_element(
            by=By.ID,
            locator='recaptcha-verify-button',
            timeout=5,
        )

        self._js_click(verify_button)

        if self._delay_config:
            self._delay_config.delay_after_click_verify_button()

        # Solve captcha again if an error occurs
        for i in range(5):
            try:
                self._wait_for_element(
                    by=By.CLASS_NAME,
                    locator='rc-audiochallenge-error-message',
                    timeout=1,
                )
    
                self._solve_audio_challenge(self._language)
    
                # Locate verify button again to avoid stale element reference and click it via JavaScript
                second_verify_button = self._wait_for_element(
                    by=By.ID,
                    locator='recaptcha-verify-button',
                    timeout=5,
                )
    
                self._js_click(second_verify_button)
    
            except TimeoutException:
                break
        else:
            raise RecaptchaException('Failed to solve captcha after 5 attempts')

        self._driver.switch_to.parent_frame()

    def _solve_audio_challenge(self, language: str) -> None:
        try:
            # Locate audio challenge download link
            download_link: WebElement = self._wait_for_element(
                by=By.CLASS_NAME,
                locator='rc-audiochallenge-tdownload-link',
                timeout=10,
            )

        except TimeoutException:
            raise RecaptchaException('Google has detected automated queries. Try again later.')

        # Create temporary directory and temporary files
        tmp_dir = tempfile.gettempdir()

        id_ = uuid.uuid4().hex

        mp3_file, wav_file = os.path.join(tmp_dir, f'{id_}_tmp.mp3'), os.path.join(tmp_dir, f'{id_}_tmp.wav')

        tmp_files = {mp3_file, wav_file}

        with open(mp3_file, 'wb') as f:
            link = download_link.get_attribute('href')

            audio_download = requests.get(url=link, allow_redirects=True)

            f.write(audio_download.content)

            f.close()

        # Convert MP3 to WAV format for compatibility with speech recognizer APIs
        AudioSegment.from_mp3(mp3_file).export(wav_file, format='wav')

        # Disable dynamic energy threshold to avoid failed reCAPTCHA audio transcription due to static noise
        self._recognizer.dynamic_energy_threshold = False

        with sr.AudioFile(wav_file) as source:
            audio = self._recognizer.listen(source)

            try:
                recognized_text = self._service.recognize(self._recognizer, audio, language)

            except sr.UnknownValueError:
                raise RecaptchaException('Speech recognition API could not understand audio, try again')

        # Clean up all temporary files
        for path in tmp_files:
            if os.path.exists(path):
                os.remove(path)

        # Write transcribed text to iframe's input box
        response_textbox = self._driver.find_element(By.ID, 'audio-response')

        self._human_type(element=response_textbox, text=recognized_text)

    def _js_click(self, element: WebElement) -> None:
        """
        Perform click on given web element using JavaScript.

        :param element: web element to click
        """

        self._driver.execute_script('arguments[0].click();', element)

    def _wait_for_element(
        self,
        by: str = By.ID,
        locator: Optional[str] = None,
        timeout: float = 10,
    ) -> WebElement:
        """
        Try to locate web element within given duration.

        :param by: strategy to use to locate element (see class `selenium.webdriver.common.by.By`)
        :param locator: locator that identifies the element
        :param timeout: number of seconds to wait for element before raising `TimeoutError`
        :return: located web element
        :raises selenium.common.exceptions.TimeoutException: if element is not located within given duration
        """

        return WebDriverWait(self._driver, timeout).until(ec.visibility_of_element_located((by, locator)))

    @staticmethod
    def _human_type(element: WebElement, text: str) -> None:
        """
        Types in a way reminiscent of a human, with a random delay in between 50ms to 100ms for every character
        :param element: Input element to type text to
        :param text: Input to be typed
        """

        for c in text:
            element.send_keys(c)

            time.sleep(random.uniform(0.05, 0.1))


# Add alias for backwards compatibility
API = RecaptchaSolver
