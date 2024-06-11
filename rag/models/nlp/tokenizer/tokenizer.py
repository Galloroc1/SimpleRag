import jieba
from typing import Union,List
from rag.fileQA.base import MetaData,Document


class BaseTokenizer:
    name = None


class TokenizerJieba(BaseTokenizer):
    name = "TokenizerJieba"

    def __init__(self):
        pass

    def tokenize(self,sentence:Union[MetaData,str]):
        if isinstance(sentence,MetaData):
            sentence = sentence.meta
        return list(jieba.cut(sentence))

    def tokenize_multi(self,sentences:Document):
        return list(map(lambda x:self.tokenize(x),sentences))
