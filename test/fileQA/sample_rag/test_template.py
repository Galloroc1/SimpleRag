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
from rag.fileQA.template import PromptTemplateRAG,apply_prompt_template


if __name__ == '__main__':
    question = "天龙八部中的龙指什么?"

    # load txt
    data_loader = TxtLoader("/home/hr/pyproject/SampleRag/samples/天龙八部.txt")
    data:Document = data_loader.load()

    # split txt
    spliter = CharacterSplitter(chunk_size=2000)
    knowledge:Document = spliter.split_document(data)

    # rank get top 20
    rank = RankEmbedding()
    knowledge = rank.topk(question=question, knowledge=knowledge,k=20)

    # rerank get top 3
    rerank = RerankerBge()
    top_k:Document = rerank.topk(question=question, knowledge=knowledge,k=3)

    # apply prompt template
    template = apply_prompt_template(prompt=PromptTemplateRAG(),question=question,knowledge=top_k)

    # get answer from Qwen
    model = QwenApi()
    now_response, history = model.chat(template, history=None)

    print(now_response)
    print("*"*100)
    # question = "你没有给出参考来源"
    # now_response, _ = model.chat(question, history=history)
    #
    # print(now_response)


