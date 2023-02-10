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
    def recognize(self, recognizer: sr.Recognizer, audio_data: AudioData) -> Any:
        """Perform speech recognition on the given audio data using the given recognizer."""
        pass


class AmazonService(Service):
    """
    Service for Amazon Transcribe.

    See docs for `speech_recognition.Recognizer.recognize_amazon` for details on congfiguration.
    """

    def __init__(
        self,
        access_key_id: Optional[Any] = None,
        secret_access_key: Optional[Any] = None,
    ) -> None:
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key

    def recognize(self, recognizer: sr.Recognizer, audio_data: AudioData) -> Any:
        return recognizer.recognize_amazon(
            audio_data,
            access_key_id=self.access_key_id,
            secret_access_key=self.secret_access_key,
        )


class AssemblyAIService(Service):
    """
    Service for AssemblyAI STT.

    See docs for `speech_recognition.Recognizer.recognize_assemblyai` for details on congfiguration.
    """

    def __init__(
        self,
        api_token: Any,
    ) -> None:
        self.api_token = api_token

    def recognize(self, recognizer: sr.Recognizer, audio_data: AudioData) -> Any:
        return recognizer.recognize_assemblyai(audio_data, api_token=self.api_token)


class AzureService(Service):
    """
    Service for Microsoft Azure Speech API.

    See docs for `speech_recognition.Recognizer.recognize_azure` for details on congfiguration.
    """

    def __init__(
        self,
        key: Any,
    ) -> None:
        self.key = key

    def recognize(self, recognizer: sr.Recognizer, audio_data: AudioData) -> Any:
        return recognizer.recognize_azure(audio_data, key=self.key)


class BingService(Service):
    """
    Service for Microsoft Bing Speech API.

    See docs for `speech_recognition.Recognizer.recognize_bing` for details on congfiguration.
    """

    def __init__(
        self,
        key: Any,
    ) -> None:
        self.key = key

    def recognize(self, recognizer: sr.Recognizer, audio_data: AudioData) -> Any:
        return recognizer.recognize_bing(audio_data, key=self.key)


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

    def recognize(self, recognizer: sr.Recognizer, audio_data: AudioData) -> Any:
        return recognizer.recognize_google(audio_data, key=self.key)


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

    def recognize(self, recognizer: sr.Recognizer, audio_data: AudioData) -> Any:
        return recognizer.recognize_google_cloud(
            audio_data, credentials_json=self.credentials_json
        )


class HoundifyService(Service):
    """
    Service for Houndify API.

    See docs for `speech_recognition.Recognizer.recognize_houndify` for details on congfiguration.
    """

    def __init__(
        self,
        client_id: Any,
        client_key: Any,
    ) -> None:
        self.client_id = client_id
        self.client_key = client_key

    def recognize(self, recognizer: sr.Recognizer, audio_data: AudioData) -> Any:
        return recognizer.recognize_houndify(
            audio_data, client_id=self.client_id, client_key=self.client_key
        )


class IbmService(Service):
    """
    Service for IBM Speech to Text API.

    See docs for `speech_recognition.Recognizer.recognize_ibm` for details on congfiguration.
    """

    def __init__(
        self,
        key: Any,
    ) -> None:
        self.key = key

    def recognize(self, recognizer: sr.Recognizer, audio_data: AudioData) -> Any:
        return recognizer.recognize_ibm(audio_data, key=self.key)


class LexService(Service):
    """
    Service for Amazon Lex API.

    See docs for `speech_recognition.Recognizer.recognize_lex` for details on congfiguration.
    """

    def __init__(
        self,
        bot_name: Any,
        bot_alias: Any,
        user_id: Any,
        access_key_id: Optional[Any] = None,
        secret_access_key: Optional[Any] = None,
    ) -> None:
        self.bot_name = bot_name
        self.bot_alias = bot_alias
        self.user_id = user_id
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key

    def recognize(self, recognizer: sr.Recognizer, audio_data: AudioData) -> Any:
        return recognizer.recognize_lex(
            audio_data,
            bot_name=self.bot_name,
            bot_alias=self.bot_alias,
            user_id=self.user_id,
            access_key_id=self.access_key_id,
            secret_access_key=self.secret_access_key,
        )


class SphinxService(Service):
    """
    Service for CMU Sphinx.

    See docs for `speech_recognition.Recognizer.recognize_sphinx` for details on congfiguration.
    """

    def __init__(
        self,
        grammar: Any = None,
    ) -> None:
        self.grammar = grammar

    def recognize(self, recognizer: sr.Recognizer, audio_data: AudioData) -> Any:
        return recognizer.recognize_sphinx(audio_data, grammar=self.grammar)


class TensorFlowService(Service):
    """
    Service for TensorFlow.

    See docs for `speech_recognition.Recognizer.recognize_tensorflow` for details on congfiguration.
    """

    def __init__(
        self,
        tensor_graph: str,
    ) -> None:
        self.tensor_graph = tensor_graph

    def recognize(self, recognizer: sr.Recognizer, audio_data: AudioData) -> Any:
        return recognizer.recognize_tensorflow(
            audio_data, tensor_graph=self.tensor_graph
        )


class VoskService(Service):
    """
    Service for Vosk.

    See docs for `speech_recognition.Recognizer.recognize_vosk` for details on congfiguration.
    """

    def __init__(
        self,
    ) -> None:
        pass

    def recognize(self, recognizer: sr.Recognizer, audio_data: AudioData) -> Any:
        return recognizer.recognize_vosk(audio_data)


class WhisperService(Service):
    """
    Service for Whisper.

    See docs for `speech_recognition.Recognizer.recognize_whisper` for details on congfiguration.
    """

    def __init__(
        self,
        model: str = "base",
    ) -> None:
        self.model = model

    def recognize(self, recognizer: sr.Recognizer, audio_data: AudioData) -> Any:
        return recognizer.recognize_whisper(audio_data, model=self.model)


class WitService(Service):
    """
    Service for Wit.ai API.

    See docs for `speech_recognition.Recognizer.recognize_wit` for details on congfiguration.
    """

    def __init__(
        self,
        key: Any,
    ) -> None:
        self.key = key

    def recognize(self, recognizer: sr.Recognizer, audio_data: AudioData) -> Any:
        return recognizer.recognize_wit(audio_data, key=self.key)
