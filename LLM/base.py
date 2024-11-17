from dataclasses import dataclass
from abc import ABC, abstractmethod


class BaseChatModel(ABC):
    MODEL_NAME = None

    @abstractmethod
    def chat(self,**kwargs):
        pass

    @abstractmethod
    def stream_chat(self,**kwargs):
        pass

    @abstractmethod
    def apply_chat_template(self,**kwargs):
        pass


@dataclass
class GenerateParams:
    top_k = 1.0
    top_p = 0.8
    max_lens = 2048
