from typing import Any, Optional

from abc import ABC, abstractmethod
import speech_recognition as sr


class Service(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def recognize(self, recognizer: sr.Recognizer) -> Any:
        pass


class AmazonService(Service):
    def __init__(
        self,
        access_key_id: Optional[Any] = None,
        secret_access_key: Optional[Any] = None,
    ) -> None:
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key

    def recognize(self, recognizer: sr.Recognizer) -> Any:
        return recognizer.recognize_amazon(self.access_key_id, self.secret_access_key)


class AssemblyAIService(Service):
    def __init__(
        self,
        api_token: Any,
    ) -> None:
        self.api_token = api_token

    def recognize(self, recognizer: sr.Recognizer) -> Any:
        return recognizer.recognize_assemblyai(self.api_token)


class AzureService(Service):
    def __init__(
        self,
        key: Any,
    ) -> None:
        self.key = key

    def recognize(self, recognizer: sr.Recognizer) -> Any:
        return recognizer.recognize_azure(self.key)


class BingService(Service):
    def __init__(
        self,
        key: Any,
    ) -> None:
        self.key = key

    def recognize(self, recognizer: sr.Recognizer) -> Any:
        return recognizer.recognize_bing(self.key)


class GoogleService(Service):
    def __init__(
        self,
        key: Optional[Any] = None,
    ) -> None:
        self.key = key

    def recognize(self, recognizer: sr.Recognizer) -> Any:
        return recognizer.recognize_google(self.key)


class GoogleCloudService(Service):
    def __init__(
        self,
        credentials_json: Optional[Any] = None,
    ) -> None:
        self.credentials_json = credentials_json

    def recognize(self, recognizer: sr.Recognizer) -> Any:
        return recognizer.recognize_google_cloud(self.credentials_json)


class HoundifyService(Service):
    def __init__(
        self,
        client_id: Any,
        client_key: Any,
    ) -> None:
        self.client_id = client_id
        self.client_key = client_key

    def recognize(self, recognizer: sr.Recognizer) -> Any:
        return recognizer.recognize_houndify(self.client_id, self.client_key)


class IbmService(Service):
    def __init__(
        self,
        key: Any,
    ) -> None:
        self.key = key

    def recognize(self, recognizer: sr.Recognizer) -> Any:
        return recognizer.recognize_ibm(self.key)


class LexService(Service):
    def __init__(
        self,
        access_key_id: Optional[Any] = None,
        secret_access_key: Optional[Any] = None,
    ) -> None:
        self.client_id = access_key_id
        self.client_key = secret_access_key

    def recognize(self, recognizer: sr.Recognizer) -> Any:
        return recognizer.recognize_lex(self.client_id, self.client_key)


class SphinxService(Service):
    def __init__(
        self,
        grammar: Optional[Any] = None,
    ) -> None:
        self.grammar = grammar

    def recognize(self, recognizer: sr.Recognizer) -> Any:
        return recognizer.recognize_sphinx(self.grammar)


class TensorFlowService(Service):
    def __init__(
        self,
        tensor_graph: str,
    ) -> None:
        self.tensor_graph = tensor_graph

    def recognize(self, recognizer: sr.Recognizer) -> Any:
        return recognizer.recognize_tensorflow(self.tensor_graph)


class VoskService(Service):
    def __init__(
        self,
    ) -> None:
        pass

    def recognize(self, recognizer: sr.Recognizer) -> Any:
        return recognizer.recognize_vosk()


class Whisperervice(Service):
    def __init__(
        self,
        model: str = "base",
    ) -> None:
        self.model = model

    def recognize(self, recognizer: sr.Recognizer) -> Any:
        return recognizer.recognize_whisper(self.model)


class WitService(Service):
    def __init__(
        self,
        key: Any,
    ) -> None:
        self.key = key

    def recognize(self, recognizer: sr.Recognizer) -> Any:
        return recognizer.recognize_wit(self.key)
