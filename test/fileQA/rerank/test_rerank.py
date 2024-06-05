import os
import sys
from pathlib import Path
root_path = str(Path.cwd().parents[2])
sys.path.append(root_path)
from rag.fileQA.loader.file_loader import TxtLoader
from rag.fileQA.text_splitter.splitter import CharacterSplitter
from rag.fileQA.rerank.rerank import RerankerBge
from rag.fileQA.rank import RankEmbedding
from rag.fileQA.base import Document
from rich import  print
if __name__ == '__main__':
    data_loader = TxtLoader("/home/hr/pyproject/SampleRag/samples/天龙八部.txt")
    spliter = CharacterSplitter()
    data:Document = data_loader.load()
    knowledge:Document = spliter.split_document(data)

    question = "天龙八部中的龙指什么?"
    rank = RankEmbedding(question=question, knowledge=knowledge)
    rank.rank()
    knowledge = rank.topk(5)
    print(rank.scores)
    rag = RerankerBge(question=question, knowledge=knowledge)
    rag.rank()
    top_k = rag.topk(3)
    print(rag.scores)

