from rag.models.nlp.embeddings.embedding import BaseEmbedding, EmbeddingBgeM3
import numpy as np
from rank_bm25 import BM25Okapi
from rag.models.nlp.tokenizer.tokenizer import BaseTokenizer, TokenizerJieba
from typing import List, Union
from rag.fileQA.base import Document

SIMILARITY = {
    "cos": "cos"
}


class BaseRank:

    def _rank(self, question: str, knowledge: Document):
        raise

    def topk(self, question, knowledge, k=5) -> Document:
        _, scores_sort_arg = self._rank(question, knowledge)
        return knowledge[scores_sort_arg[0:k]]


class RankEmbedding(BaseRank):

    def __init__(self,
                 similar="cos",
                 embedding=EmbeddingBgeM3,
                 ):
        self.similar = similar
        self.embedding = embedding()

    def _rank(self, question: str, knowledge: Document):
        knowledge_embeddings = self.embedding.encode_document(knowledge)
        question_embeddings = self.embedding.encode([question])
        scores = (question_embeddings @ knowledge_embeddings.T)[0]
        scores_sort_arg = np.argsort(scores)[::-1]
        return scores, scores_sort_arg


class RankBM25(BaseRank):

    def __init__(self,
                 tokenizer=TokenizerJieba,
                 ):
        self.tokenizer = tokenizer()

    def _rank(self, question: str, knowledge: Document):
        tokenized_documents = self.tokenizer.tokenize_multi(knowledge)
        bm25 = BM25Okapi(tokenized_documents)
        tokenized_query = self.tokenizer.tokenize(question)
        scores = np.array(bm25.get_scores(tokenized_query))
        scores_sort_arg = np.argsort(scores)[::-1]
        return scores, scores_sort_arg
