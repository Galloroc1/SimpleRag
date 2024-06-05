from FlagEmbedding import FlagReranker
from rag.fileQA.base import MetaData,Document
from rag.fileQA.rank import BaseRank
from typing import List
import numpy as np


class RerankerBge(BaseRank):

    def __init__(self):
        self.reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True)

    def _rank(self,question:str,knowledge:Document ):
        # You can map the scores into 0-1 by set "normalize=True", which will apply sigmoid function to the score
        paris = list(map(lambda x: (x[0], x[1].meta), zip([question] * len(knowledge), knowledge.metas)))
        scores = self.reranker.compute_score(paris, normalize=True)
        scores_sort_arg = np.argsort(scores)[::-1]
        return scores,scores_sort_arg



