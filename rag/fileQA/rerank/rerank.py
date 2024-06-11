from FlagEmbedding import FlagReranker
from rag.fileQA.base import MetaData,Document
from rag.fileQA.rank import BaseRank
from typing import List,Dict
import numpy as np
from functools import reduce


class RerankerBge(BaseRank):
    name = "RerankerBge"

    def __init__(self):
        self.reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True)
        self.name = self.name + "bge-reranker-v2-m3"

    def _rank(self,question:str,knowledge:Document ):
        # You can map the scores into 0-1 by set "normalize=True", which will apply sigmoid function to the score
        paris = list(map(lambda x: (x[0], x[1].meta), zip([question] * len(knowledge), knowledge.metas)))
        scores = self.reranker.compute_score(paris, normalize=True)
        scores_sort_arg = np.argsort(scores)[::-1]
        return scores,scores_sort_arg


class RerankerRRF(BaseRank):
    name = 'rrf'

    def __init__(self, f_k=10):
        self.f_k = f_k

    def _rank(self,question,knowledge:List[Document])->Dict[MetaData,float]:
        def _get_rank_score(k: Document)->Dict:
            lens = len(k)
            source_dict = {}
            for index,meta in enumerate(k):
                source_dict.update({meta:1-index/lens})
            return source_dict

        def _update(item1:Dict,item2:Dict):
            for key,value in item2.items():
                if key in item1:
                    item1[key] = item1[key] + item2[key]
                else:
                    item1[key] = item2[key]
            return item1

        scores = list(map(_get_rank_score, knowledge))
        score_dict = reduce(lambda item1, item2: _update(item1,item2), scores)
        sorted_dict = dict(sorted(score_dict.items(), key=lambda item: item[1],reverse=True))
        return sorted_dict

    def topk(self, question, knowledge, k=5) -> Document:
        scores_sort_arg = self._rank(question, knowledge)
        scores = list(scores_sort_arg.values())[0:k]
        metas = list(scores_sort_arg.keys())[0:k]
        for i,value in enumerate(metas):
            value.score = scores[i]
            value.source.update({"rank":self.name})

        document = Document(metas,
                        source={"path":"multi_path","rank":"rerank by RRF"})
        return document





