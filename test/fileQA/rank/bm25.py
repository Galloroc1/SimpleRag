import os
import sys
from pathlib import Path
root_path = str(Path.cwd().parents[2])
sys.path.append(root_path)
from rag.fileQA.loader.file_loader import TxtLoader
from rag.fileQA.text_splitter.splitter import CharacterSplitter
from rag.fileQA.rank.rank import RankBM25
from rag.fileQA.base import Document
from rich import  print

if __name__ == '__main__':
    data_loader = TxtLoader(os.path.join(root_path,"samples/天龙八部.txt"))
    spliter = CharacterSplitter()
    data:Document = data_loader.load()
    knowledge:Document = spliter.split_document(data)

    question = "天龙八部中的龙指什么?"
    rag = RankBM25()
    top_k = rag.topk(question=question, knowledge=knowledge,k=5)
    print(top_k)
