from typing import Any, Optional
from abc import ABC, abstractmethod
from speech_recognition import AudioData
import speech_recognition as sr


class Service(ABC):
    """Abstract base class for speech recognition services."""

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def recognize(self, recognizer: sr.Recognizer, audio_data: AudioData, language: str = 'en-US') -> Any:
        """Perform speech recognition on the given audio data using the given recognizer."""
        pass


class GoogleService(Service):
    """
    Service for Google Speech Recognition API.

    See docs for `speech_recognition.Recognizer.recognize_google` for details on congfiguration.
    """

    def __init__(
        self,
        key: Optional[Any] = None,
    ) -> None:
        self.key = key

    def recognize(self, recognizer: sr.Recognizer, audio_data: AudioData, language: str = 'en-US') -> Any:
        return recognizer.recognize_google(audio_data, key=self.key, language=language)


class GoogleCloudService(Service):
    """
    Service for Google Cloud Speech API.

    See docs for `speech_recognition.Recognizer.recognize_google_cloud` for details on congfiguration.
    """

    def __init__(
        self,
        credentials_json: Optional[Any] = None,
    ) -> None:
        self.credentials_json = credentials_json

    def recognize(self, recognizer: sr.Recognizer, audio_data: AudioData, language: str = 'en-US') -> Any:
        return recognizer.recognize_google_cloud(
            audio_data, credentials_json=self.credentials_json
        )
