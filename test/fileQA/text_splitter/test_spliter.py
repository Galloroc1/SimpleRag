import os
import sys
sys.path.append("/home/hr/pyproject/SampleRag/")
from rag.fileQA.loader.file_loader import TxtLoader
from rag.fileQA.text_splitter.splitter import CharacterSplitter
from rich import print

def test_text_loader(path):
    data = TxtLoader(path).load()
    data = CharacterSplitter().split_document(data)
    for i in data:
        print(i)
if __name__ == '__main__':
    test_text_loader("/samples/天龙八部.txt")
