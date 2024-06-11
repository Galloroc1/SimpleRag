from rag.fileQA.rank.rank import BaseRank
from typing import List


class RankerPipe:

    def __init__(self,rankers:List[BaseRank]):
        self.rankers = rankers

    def topk(self,question,knowledge,k=5):
        pass

