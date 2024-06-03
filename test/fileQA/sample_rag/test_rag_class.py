import os
import sys
sys.path.append("/home/hr/pyproject/SampleRag/")
from rag.fileQA.loader.file_loader import TxtLoader
from rag.fileQA.core import BaseRetrievalAugmentedByEmbedding
from rich import  print
if __name__ == '__main__':
    data_loader = TxtLoader("/home/hr/pyproject/SampleRag/samples/天龙八部.txt")
    question = ["天龙八部中的龙指什么?","八部指什么"]
    rag = BaseRetrievalAugmentedByEmbedding(question=question,loader=data_loader)
    rag.compute_similarity()
    top_k = rag.topk(5)
    knowledge = rag.knowledge[top_k]
    print(knowledge[1])