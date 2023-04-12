from abc import ABC, abstractmethod
import random
import time


class DelayConfig(ABC):
    """Abstract base class for delay configurations for :class:`RecaptchaSolver`."""

    @abstractmethod
    def delay_after_click_checkbox(self):
        pass

    @abstractmethod
    def delay_after_click_audio_button(self):
        pass

    @abstractmethod
    def delay_after_click_verify_button(self):
        pass


class StandardDelayConfig(DelayConfig):
    def __init__(self, min_delay: float = 0.75, max_delay: float = 1.25) -> None:
        self.min_delay = min_delay
        self.max_delay = max_delay

    def _sleep_random(self) -> None:
        time.sleep(random.uniform(self.min_delay, self.max_delay))

    def delay_after_click_checkbox(self):
        self._sleep_random()

    def delay_after_click_audio_button(self):
        self._sleep_random()

    def delay_after_click_verify_button(self):
        self._sleep_random()
