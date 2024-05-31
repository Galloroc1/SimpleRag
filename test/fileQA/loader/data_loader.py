import os
import sys
current_path = os.getcwd()
root_path = current_path[:current_path.find('rag')]+"rag"
sys.path.append(root_path)
from rag.fileQA.loader.file_loader import TxtLoader


def test_text_loader(path):
    data = TxtLoader(path).load()
    print(data[0])


if __name__ == '__main__':
    test_text_loader("/home/hr/pyproject/rag/samples/txt_test.txt")
