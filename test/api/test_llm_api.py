import os
import sys
from pathlib import Path
root_path = str(Path.cwd().parents[2])
sys.path.append(root_path)
from rag.models.nlp.LLM.api import QwenApi
# from rich import print

if __name__ == '__main__':
    model = QwenApi()
    now_response,history = model.chat("如何做西红柿炖牛腩",history=None)
    print(now_response)
    now_response,history = model.chat("不放糖行吗？",history=history)
    print(now_response)
    print("*"*100)

