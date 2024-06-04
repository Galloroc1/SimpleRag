from FlagEmbedding import FlagReranker
from rag.fileQA.base import MetaData,Document
from typing import List


class BaseRerank:

    def __init__(self,doc):
        pass


class Reranker:

    def __init__(self,question:str,doc:Document):
        self.reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True)

    def rerank(self,question,):
        reranker = None
        score = reranker.compute_score(['query', 'passage'])
        print(score) # -5.65234375

        # You can map the scores into 0-1 by set "normalize=True", which will apply sigmoid function to the score
        score = reranker.compute_score(['query', 'passage'], normalize=True)
        print(score) # 0.003497010252573502

        scores = reranker.compute_score([['what is panda?', 'hi'], ['what is panda?', 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.']])
        print(scores) # [-8.1875, 5.26171875]

        # You can map the scores into 0-1 by set "normalize=True", which will apply sigmoid function to the score
        scores = reranker.compute_score([['what is panda?', 'hi'],
                                         ['what is panda?', 'The giant panda (Ailuropoda melanoleuca), '
                                                            'sometimes called a panda bear or simply panda, '
                                                            'is a bear species endemic to China.']], normalize=True)

