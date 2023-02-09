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
    def recognize(self, recognizer: sr.Recognizer, audio: AudioData) -> Any:
        """Perform speech recognition on the given audio data using the given recognizer."""
        pass


class BingService(Service):
    """Service for Microsoft Bing Speech API.

    See docs for `speech_recognition.Recognizer.recognize_bing` for more information on credentials.
    """

    def __init__(
        self,
        key: Any,
    ) -> None:
        self.key = key

    def recognize(self, recognizer: sr.Recognizer, audio: AudioData) -> Any:
        return recognizer.recognize_bing(audio, key=self.key)


class GoogleService(Service):
    """Service for Google Speech Recognition API.

    See docs for `speech_recognition.Recognizer.recognize_google` for more information on credentials.
    """

    def __init__(
        self,
        key: Optional[Any] = None,
    ) -> None:
        self.key = key

    def recognize(self, recognizer: sr.Recognizer, audio: AudioData) -> Any:
        return recognizer.recognize_google(audio, key=self.key)


class GoogleCloudService(Service):
    """Service for Google Cloud Speech API.

    See docs for `speech_recognition.Recognizer.recognize_google_cloud` for more information on credentials.
    """

    def __init__(
        self,
        credentials_json: Optional[Any] = None,
    ) -> None:
        self.credentials_json = credentials_json

    def recognize(self, recognizer: sr.Recognizer, audio: AudioData) -> Any:
        return recognizer.recognize_google_cloud(
            audio, credentials_json=self.credentials_json
        )


class HoundifyService(Service):
    """Service for Houndify API.

    See docs for `speech_recognition.Recognizer.recognize_houndify` for more information on credentials.
    """

    def __init__(
        self,
        client_id: Any,
        client_key: Any,
    ) -> None:
        self.client_id = client_id
        self.client_key = client_key

    def recognize(self, recognizer: sr.Recognizer, audio: AudioData) -> Any:
        return recognizer.recognize_houndify(
            audio, client_id=self.client_id, client_key=self.client_key
        )


class IbmService(Service):
    """Service for IBM Speech to Text API.

    See docs for `speech_recognition.Recognizer.recognize_google_cloud` for more information on credentials.
    """

    def __init__(
        self,
        key: Any,
    ) -> None:
        self.key = key

    def recognize(self, recognizer: sr.Recognizer, audio: AudioData) -> Any:
        return recognizer.recognize_ibm(audio, key=self.key)


class SphinxService(Service):
    """Service for CMU Sphinx.

    See docs for `speech_recognition.Recognizer.recognize_sphinx` for more information on credentials.
    """

    def __init__(
        self,
        grammar: Any = None,
    ) -> None:
        self.grammar = grammar

    def recognize(self, recognizer: sr.Recognizer, audio: AudioData) -> Any:
        return recognizer.recognize_sphinx(audio, grammar=self.grammar)


class WitService(Service):
    """Service for Wit.ai API.

    See docs for `speech_recognition.Recognizer.recognize_wit` for more information on credentials.
    """

    def __init__(
        self,
        key: Any,
    ) -> None:
        self.key = key

    def recognize(self, recognizer: sr.Recognizer, audio: AudioData) -> Any:
        return recognizer.recognize_wit(audio, key=self.key)
