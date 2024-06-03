import os
import sys
sys.path.append("/home/hr/pyproject/SampleRag/")
from rag.fileQA.loader.file_loader import TxtLoader


def test_text_loader(path):
    data = TxtLoader(path).load()
    print(data[0])


if __name__ == '__main__':
    test_text_loader("/home/hr/pyproject/rag/samples/天龙八部.txt")
