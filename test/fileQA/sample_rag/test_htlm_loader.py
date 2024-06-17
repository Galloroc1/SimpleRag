import os
import sys
from pathlib import Path
root_path = str(Path.cwd().parents[2])
sys.path.append(root_path)
from rag.fileQA.loader.file_loader import HtmlLoader
from rag.fileQA.text_splitter.splitter import CharacterSplitter
from rag.models.nlp.embeddings.embedding import EmbeddingBgeM3
from rich import print
import numpy as np
from rag.models.nlp.LLM.api import QwenApi


def get_answer(question,kl):
    template = (f"请你根据用户问题和用户提供的参考资料回答问题，同时输出参考文件的来源，要求内容准确、不允许胡编乱造。"
                f"限制：如果用户提供的资料不具备参考意义，你可以不必参考，但是需要给用户说明，说明语为：您的参考资料似乎跟问题无关。"
                +f"用户的参考资料如下:\n{str(kl.meta)}\n"
                +f"参考来源：路径{kl.source['path']}、"
                +f"其中用户的问题如下:\n{question}"
                )
    print(template)
    model = QwenApi()
    now_response, _ = model.chat(template, history=None)
    return now_response


if __name__ == '__main__':
    path = "https://python.langchain.com/v0.2/docs/introduction/"
    question = "langchain是什么"
    sentence = HtmlLoader(path).load()
    print(f"sentence↓\n{sentence}")
    now_response = get_answer(question, sentence[0])
    print("question:",question)
    print(now_response)
