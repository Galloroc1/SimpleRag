from rag.fileQA.loader.file_loader import TxtLoader, BaseDataLoader
from rag.fileQA.text_splitter.splitter import CharacterSplitter, BaseSplitter
from rag.models.nlp.embeddings.embedding import BaseEmbedding,EmbeddingBgeM3
from abc import ABC, abstractmethod
from typing import List
from rag.fileQA.base import MetaData, Document
import numpy as np

SIMILARITY = {
    "cos": "cos"
}


class BaseRetrievalAugmentedByEmbedding():

    def __init__(self,
                 question: List[str],
                 loader: BaseDataLoader,
                 similarity="cos",
                 embedding: BaseEmbedding = EmbeddingBgeM3(),
                 splitter: BaseSplitter = CharacterSplitter(),
                 ):
        self.question = question
        self.similarity = SIMILARITY[similarity]
        self.embedding = embedding
        self.loader = loader
        self.splitter = splitter
        # todo: reranker not support now
        self.reranker = None
        self.k = 5

        self.knowledge = None
        self.scores = None
        self.scores_sort_arg = None

    def compute_similarity_with_document(self):
        knowledge_embeddings = self.embedding.encode_document(self.knowledge)
        question_embeddings = self.embedding.encode(self.question)
        self.scores = question_embeddings @ knowledge_embeddings.T
        self.scores_sort_arg = np.argsort(self.scores, axis=1)

    def sparse_meta_file(self):
        knowledge = self.loader.load()
        self.knowledge = self.splitter.split_document(document=knowledge)

    def compute_similarity(self,):
        self.sparse_meta_file()
        self.compute_similarity_with_document()

    def topk(self, k=5):
        self.k = k if k else self.k
        if self.knowledge is None or self.scores is None:
            raise AttributeError("you should compute similarity before")
        top_k_args = self.scores_sort_arg[:, -k:][:,::-1]
        return self.knowledge[top_k_args]
