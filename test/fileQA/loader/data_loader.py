import os
import sys
from pathlib import Path

current_path = str(Path(sys.path[0]).resolve().parents[2])
sys.path.append(current_path)
from rag.fileQA.loader.file_loader import TxtLoader,DocxLoader


def test_text_loader(path):
    data = TxtLoader(path).load()
    print(data[0])

def test_doc_loader(path):
    data = DocxLoader(path).load()
    print(data[0])

if __name__ == '__main__':
    # test_text_loader(os.path.join(current_path, 'samples', '天龙八部.txt'))
    test_doc_loader(os.path.join(current_path,"samples","刑法.docx"))