from typing import Any, Optional
from abc import ABC, abstractmethod
from speech_recognition import AudioData
import speech_recognition as sr


class Service(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def recognize(self, recognizer: sr.Recognizer, audio: AudioData) -> Any:
        pass


class BingService(Service):
    def __init__(
        self,
        key: Any,
    ) -> None:
        self.key = key

    def recognize(self, recognizer: sr.Recognizer, audio: AudioData) -> Any:
        return recognizer.recognize_bing(audio, key=self.key)


class GoogleService(Service):
    def __init__(
        self,
        key: Optional[Any] = None,
    ) -> None:
        self.key = key

    def recognize(self, recognizer: sr.Recognizer, audio: AudioData) -> Any:
        return recognizer.recognize_google(audio, key=self.key)


class GoogleCloudService(Service):
    def __init__(
        self,
        credentials_json: Optional[Any] = None,
    ) -> None:
        self.credentials_json = credentials_json

    def recognize(self, recognizer: sr.Recognizer, audio: AudioData) -> Any:
        return recognizer.recognize_google_cloud(audio, credentials_json=self.credentials_json)


class HoundifyService(Service):
    def __init__(
        self,
        client_id: Any,
        client_key: Any,
    ) -> None:
        self.client_id = client_id
        self.client_key = client_key

    def recognize(self, recognizer: sr.Recognizer, audio: AudioData) -> Any:
        return recognizer.recognize_houndify(audio, client_id=self.client_id, client_key=self.client_key)


class IbmService(Service):
    def __init__(
        self,
        key: Any,
    ) -> None:
        self.key = key

    def recognize(self, recognizer: sr.Recognizer, audio: AudioData) -> Any:
        return recognizer.recognize_ibm(audio, key=self.key)


class SphinxService(Service):
    def __init__(
        self,
        language: str = None,
        grammar: Any = None,
    ) -> None:
        self.language = language
        self.grammar = grammar

    def recognize(self, recognizer: sr.Recognizer, audio: AudioData) -> Any:
        return recognizer.recognize_sphinx(audio, language=self.language, grammar=self.grammar)


class WitService(Service):
    def __init__(
        self,
        key: Any,
    ) -> None:
        self.key = key

    def recognize(self, recognizer: sr.Recognizer, audio: AudioData) -> Any:
        return recognizer.recognize_wit(audio, key=self.key)
