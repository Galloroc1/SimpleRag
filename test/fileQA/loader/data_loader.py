import os
import sys
from pathlib import Path
root_path = str(Path.cwd().parents[2])
sys.path.append(root_path)
from rag.fileQA.loader.file_loader import TxtLoader


def test_text_loader(path):
    data = TxtLoader(path).load()
    print(data[0])


if __name__ == '__main__':
    test_text_loader("/home/hr/pyproject/SampleRag/samples/天龙八部.txt")
