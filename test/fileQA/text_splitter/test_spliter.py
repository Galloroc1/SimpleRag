import os
import sys
from pathlib import Path
root_path = str(Path.cwd().parents[2])
sys.path.append(root_path)
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
