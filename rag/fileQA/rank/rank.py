from rag.models.nlp.embeddings.embedding import BaseEmbedding,EmbeddingBgeM3
import numpy as np
from rank_bm25 import BM25Okapi
from rag.models.nlp.tokenizer.tokenizer import BaseTokenizer,TokenizerJieba
from typing import List,Union
from rag.fileQA.base import Document

SIMILARITY = {
    "cos": "cos"
}


class BaseRank:
    question = None
    knowledge = None
    scores = None
    scores_sort_arg = None

    def rank(self):
        pass


    def topk(self,k=5)->Document:
        if self.knowledge is None or self.scores is None:
            raise AttributeError("you should compute similarity before")
        top_k_args = self.scores_sort_arg[0:k]
        return self.knowledge[top_k_args]


class RankEmbedding(BaseRank):

    def __init__(self,
                 question: str,
                 knowledge:Document,
                 similar="cos",
                 embedding=EmbeddingBgeM3,
                 ):
        self.question = question
        self.knowledge = knowledge
        self.similar = similar
        self.embedding = embedding()


    def rank(self,):
        knowledge_embeddings = self.embedding.encode_document(self.knowledge)
        question_embeddings = self.embedding.encode([self.question])
        self.scores = (question_embeddings @ knowledge_embeddings.T)[0]
        self.scores_sort_arg = np.argsort(self.scores)[::-1]



class RankBM25(BaseRank):

    def __init__(self,
                 question:str,
                 knowledge: Document,
                 tokenizer =TokenizerJieba,
                 ):
        self.question = question
        self.knowledge = knowledge
        self.tokenizer = tokenizer()


    def rank(self):
        tokenized_documents = self.tokenizer.tokenize_multi(self.knowledge)
        bm25 = BM25Okapi(tokenized_documents)
        tokenized_query = self.tokenizer.tokenize(self.question)
        self.scores = np.array(bm25.get_scores(tokenized_query))
        self.scores_sort_arg = np.argsort(self.scores)[::-1]

