import os
import sys
from pathlib import Path

root_path = str(Path.cwd().parents[0])
sys.path.append(root_path)
from rag.fileQA.rewrite.rewriter import PromptTemplateRewriterSubq
from rich import print
from llm.api import QwenApi
from rag.fileQA.loader.file_loader import DocxLoader
from rag.fileQA.text_splitter.splitter import BaseSplitter
from rag.fileQA.rerank.rerank import RerankerBge, RerankerRRF
from rag.fileQA.rank import RankEmbedding
from rag.fileQA.base import Document,MetaData
from rag.fileQA.template import PromptTemplateRAG
from functools import reduce
import re


class SplitterByRe(BaseSplitter):

    def __init__(self,pattern = r'(第[\u4e00-\u9fa5]+条(?:之[\u4e00-\u9fa5]+)?)\u3000',):
        self.pattern = pattern


    def split_meta(self,meta,**kwargs):
        result = re.split(self.pattern, meta.meta)
        result = [item for item in result if item.strip()]
        sections = []
        source = []
        for i in range(0, len(result), 2):
            sections.append(result[i] + result[i + 1])
            source.append({"path":meta.source['path'],
                           "part": result[i].replace("\u3000","").replace("\n",""),
                           "part_count":"总451条"})
        new_metas = list(map(lambda new_meta, src: MetaData(new_meta, src), sections, source))
        return new_metas

    def split_document(self, document: Document,**kwargs):
        r = list(map(lambda x: self.split_meta(x), document))
        new_document = Document(reduce(lambda item1, item2: item1 + item2, r), source=document.source)
        return new_document



if __name__ == '__main__':
    print(root_path)
    data_loader = DocxLoader(os.path.join(root_path, "samples/刑法.docx"))
    spliter = SplitterByRe()
    data: Document = data_loader.load()
    knowledge: Document = spliter.split_document(data)
    rewrite_template = PromptTemplateRewriterSubq()
    rank = RankEmbedding()
    model = QwenApi()
    rrf = RerankerRRF()
    rerank = RerankerBge()
    template = PromptTemplateRAG()
    #
    test_all = False
    question = ("2020年8月22日8时许，在成都市高新区，被告人易煜为发泄情绪，将阳台处一凳子扔至楼下有大量人员、车辆的路面，"
                "并致被害人陈某1停放的一辆轿车引擎盖受损（维修费用人民币3131元）。"
                "当日，民警在宿舍将易煜挡获。另查明，2020年9月1日，易煜家人已赔偿陈某1人民币1万元，陈某1谅解易煜。"
                "易煜案发时具有部分刑事责任能力。法院认为它犯罪情节较轻，有悔罪表现，没有再犯罪的危险，适用缓刑对其所居住的社区没有重大不良影响。"
                "请问易煜应该以什么罪名被起诉，是否符合减刑标准，应该被判多少年？")
    # # question = ("就是那个谁，张三，你告诉我张三的消息")
    # # question = "光闸是什么"
    #
    if test_all:
        rewrite_questions = rewrite_template.rewrite(question, model)
        print(rewrite_questions)
        knowledges = []
        for q in rewrite_questions:
            part = rank.topk(question=q, knowledge=knowledge, k=10)
            knowledges.append(part)
        # top_k = reduce(lambda item1,item2:item1 + item2,knowledges)

        top_k = rrf.topk(question=None, knowledge=knowledges, k=10)
        top_k = rerank.topk(question=question, knowledge=top_k, k=5)
        print(top_k)

        content = "".join(f"[详细内容：{value.source['path']} 子段：第{value.source['part']}部分]:\n{value.meta}\n"
                          for value in top_k)

        prompt = template.apply(question, content)

        now_response, history = model.chat(prompt, history=None)

        print(now_response)
        print("*" * 100)
    else:
        top_k = rank.topk(question=question, knowledge=knowledge, k=10)
        top_k = rerank.topk(question=question, knowledge=top_k, k=5)
        print(top_k)
        content = "".join(f"[详细内容：{value.source['path']} 子段：第{value.source['part']}部分]:\n{value.meta}\n"
                          for value in top_k)
        prompt = template.apply(question, content)
        now_response, history = model.chat(prompt, history=None)

        print(now_response)
        print("*" * 100)