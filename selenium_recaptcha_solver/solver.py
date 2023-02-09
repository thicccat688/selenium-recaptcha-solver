from selenium_recaptcha_solver.exceptions import RecaptchaException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from pydub import AudioSegment
from typing import Any, Optional
import speech_recognition as sr
import random
import requests
import tempfile
import time
import os

from .services import Service, GoogleService


DEFAULT_SERVICE: Service = GoogleService()


class RecaptchaSolver:
    def __init__(self, driver: WebDriver, slow_mode: bool = False, service: Service = DEFAULT_SERVICE):
        """
        :param driver: Selenium web driver to use to solve the captcha
        :param slow_mode: if ``True``, sleep for brief durations between UI interactions
        :param service: service to use for speech recognition (defaults to ``GoogleService``).
            See the ``services`` module for available services.
        """

        self.__driver = driver
        self.__slow_mode = slow_mode

        # Initialise speech recognition API object
        self.__recognizer = sr.Recognizer()
        self.__service = service

    def click_recaptcha_v2(self, iframe: WebElement) -> None:
        """Click the "I'm not a robot" checkbox and then solve a reCAPTCHA v2 challenge.

        Call this method directly on web pages with an "I'm not a robot" checkbox. See <https://developers.google.com/recaptcha/docs/versions> for details of how this works.

        :param iframe: web element for inline frame of reCAPTCHA to solve
        """

        self.__driver.switch_to.frame(iframe)

        checkbox = self.__driver.find_element(
            by='id',
            value='recaptcha-anchor',
        )

        self._random_sleep()

        self._js_click(checkbox)

        if checkbox.get_attribute('checked'):
            return

        self.__driver.switch_to.parent_frame()

        captcha_challenge = self._wait_for_element(
            by=By.XPATH,
            locator='//iframe[@title="recaptcha challenge expires in two minutes"]',
            timeout=5,
        )

        self.solve_recaptcha_v2_challenge(iframe=captcha_challenge)

    def solve_recaptcha_v2_challenge(self, iframe: WebElement) -> None:
        """Solve a reCAPTCHA v2 challenge that has already appeared.

        Call this method directly on web pages with the "invisible reCAPTCHA" badge. See <https://developers.google.com/recaptcha/docs/versions> for details of how this works.

        :param iframe: web element for inline frame of reCAPTCHA to solve
        """

        self.__driver.switch_to.frame(iframe)

        # Locate captcha audio button and click it via JavaScript
        audio_button = self._wait_for_element(
            by=By.ID,
            locator='recaptcha-audio-button',
            timeout=10,
        )

        self._random_sleep()

        self._js_click(audio_button)

        self._solve_audio_challenge()

        # Locate verify button and click it via JavaScript
        verify_button = self._wait_for_element(
            by=By.ID,
            locator='recaptcha-verify-button',
            timeout=5,
        )

        self._random_sleep()

        self._js_click(verify_button)

        try:
            self._wait_for_element(
                by=By.XPATH,
                locator='//div[normalize-space()="Multiple correct solutions required - please solve more."]',
                timeout=1,
            )

            self._solve_audio_challenge()

            # Locate verify button again to avoid stale element reference and click it via JavaScript
            second_verify_button = self._wait_for_element(
                by=By.ID,
                locator='recaptcha-verify-button',
                timeout=5,
            )

            self._random_sleep()

            self._js_click(second_verify_button)

        except TimeoutException:
            pass

        self.__driver.switch_to.parent_frame()

    def _solve_audio_challenge(self) -> None:
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

        mp3_file, wav_file = os.path.join(tmp_dir, 'tmp.mp3'), os.path.join(tmp_dir, 'tmp.wav')

        tmp_files = {mp3_file, wav_file}

        with open(mp3_file, 'wb') as f:
            link = download_link.get_attribute('href')

            audio_download = requests.get(url=link, allow_redirects=True)

            f.write(audio_download.content)

            f.close()

        # Convert MP3 to WAV format for compatibility with speech recognizer APIs
        AudioSegment.from_mp3(mp3_file).export(wav_file, format='wav')

        # Disable dynamic energy threshold to avoid failed reCAPTCHA audio transcription due to static noise
        self.__recognizer.dynamic_energy_threshold = False

        with sr.AudioFile(wav_file) as source:
            audio = self.__recognizer.listen(source)

            try:
                recognized_text = self.__service.recognize(self.__recognizer, audio)

            except sr.UnknownValueError:
                raise RecaptchaException('Speech recognition API could not understand audio, try again')

        # Clean up all temporary files
        for path in tmp_files:
            if os.path.exists(path):
                os.remove(path)

        # Write transcribed text to iframe's input box
        response_textbox = self.__driver.find_element(by='id', value='audio-response')

        self._random_sleep()

        response_textbox.send_keys(recognized_text)

    def _random_sleep(self) -> None:
        if self.__slow_mode:
            time.sleep(random.randrange(1, 3))

    def _js_click(self, element: WebElement) -> None:
        """Perform click on given web element using JavaScript.

        :param element: web element to click
        """

        self.__driver.execute_script('arguments[0].click();', element)

    def _wait_for_element(
            self,
            by: str = By.ID,
            locator: Optional[str] = None,
            timeout: float = 10,
    ) -> WebElement:
        """Try to locate web element within given duration.

        :param by: strategy to use to locate element (see class `selenium.webdriver.common.by.By`)
        :param locator: locator that identifies the element
        :param timeout: number of seconds to wait for element before raising `TimeoutError`
        :return: located web element
        :raises selenium.common.exceptions.TimeoutException: if element is not located within given duration
        """

        return WebDriverWait(self.__driver, timeout).until(ec.visibility_of_element_located((by, locator)))


# Add alias for backwards compatibility
API = RecaptchaSolver
