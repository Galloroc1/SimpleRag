import os
import sys
from pathlib import Path
root_path = str(Path.cwd().parents[2])
sys.path.append(root_path)
from rag.fileQA.loader.file_loader import HtmlLoader


def test_text_loader(path):
    data = HtmlLoader(path).load()
    print(data[0])


if __name__ == '__main__':
    test_text_loader("https://www.eeo.com.cn/2024/0604/664908.shtml")
