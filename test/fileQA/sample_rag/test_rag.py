import os
import sys
from pathlib import Path
root_path = str(Path.cwd().parents[2])
sys.path.append(root_path)
from rag.fileQA.loader.file_loader import TxtLoader
from rag.fileQA.text_splitter.splitter import CharacterSplitter
from rag.fileQA.rerank.rerank import RerankerBge
from rag.fileQA.rank import RankEmbedding
from rag.fileQA.base import Document
from rich import  print
from rag.models.nlp.LLM.api import QwenApi

def get_answer(question,kl):
    template = ""
    for index,value in enumerate(kl):
        template = (template + f"参考资料{index}说明：[来源][{value.source['path']}中第{value.source['part']}部分]\n"+
                    f"详细内容：{value.meta}")

    template = (template+f"用户问题如下：{question}\n"+
                (f"请你根据用户问题和用户提供的参考资料回答问题，同时输出参考文件的来源，要求内容准确、不允许胡编乱造。"))
    model = QwenApi()
    now_response, _ = model.chat(template, history=None)
    return now_response


if __name__ == '__main__':
    data_loader = TxtLoader("/home/hr/pyproject/SampleRag/samples/天龙八部.txt")
    spliter = CharacterSplitter(chunk_size=2000)
    data:Document = data_loader.load()

    knowledge:Document = spliter.split_document(data)

    question = "天龙八部中的龙指什么?"
    rank = RankEmbedding(question=question, knowledge=knowledge)
    rank.rank()
    knowledge = rank.topk(20)

    rag = RerankerBge(question=question, knowledge=knowledge)
    rag.rank()
    top_k = rag.topk(1)
    print(top_k)
    response = get_answer(question,top_k)
    print(response)


