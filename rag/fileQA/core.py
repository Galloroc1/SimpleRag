from rag.fileQA.loader.file_loader import TxtLoader,BaseDataLoader
from rag.fileQA.text_splitter.splitter import CharacterSplitter,BaseSplitter
from rag.fileQA.embedding.embedding import BaseEmbedding,EmbeddingBgeM3
from abc import ABC,abstractmethod
from typing import List
from rag.fileQA.base import MetaData,Document
import numpy as np


SIMILARITY={
    "cos":"cos"
}

class BaseRetrievalAugmentedByEmebdding():

    def __init__(self,similarity="cos",
                 embedding:BaseEmbedding=EmbeddingBgeM3,
                 loader:BaseDataLoader = TxtLoader,
                 splitter:BaseSplitter = CharacterSplitter,
                 ):

        self.similarity = SIMILARITY[similarity]
        self.embedding = embedding
        self.loader = loader
        self.splitter = splitter
        self.k = 5

    def compute_similarity_with_document(self,question:List[str],knowledge_part:Document):
        knowledge_embeddings = self.embedding.encode_document(knowledge_part)
        question_embeddings = self.embedding.encode(question)
        scores = knowledge_embeddings @ question_embeddings.T
        return scores

    def compute_similarity(self,question:List[str]):
        knowledge = self.loader.load()
        knowledge_part = self.splitter.split_document(knowledge)
        scores = self.compute_similarity_with_document(question,knowledge_part)
        return scores

    def topk(self,question,knowledge:Document,k=5):
        self.k = k if k else self.k
