import os
import sys
from pathlib import Path
root_path = str(Path.cwd().parents[2])
sys.path.append(root_path)
from rag.fileQA.rewrite.rewriter import PromptTemplateRewriterSubq
from rich import  print
from rag.models.nlp.LLM.api import QwenApi
from rag.fileQA.loader.file_loader import TxtLoader,DocxLoader
from rag.fileQA.text_splitter.splitter import CharacterSplitter
from rag.fileQA.rerank.rerank import RerankerBge,RerankerRRF
from rag.fileQA.rank import RankEmbedding
from rag.fileQA.base import Document
from rag.fileQA.template import PromptTemplateRAG


if __name__ == '__main__':
    from functools import reduce

    print(root_path)
    data_loader = DocxLoader(os.path.join(root_path,"samples/刑法.docx"))
    spliter = CharacterSplitter(chunk_size=300)
    data: Document = data_loader.load()
    knowledge: Document = spliter.split_document(data)
    
    
    rewrite_template = PromptTemplateRewriterSubq()
    rank = RankEmbedding()
    model = QwenApi()
    rrf = RerankerRRF()
    rerank = RerankerBge()
    template = PromptTemplateRAG()

    test_all = False
    question = ("张三家住在32楼，他在阳台上放了一盆花，有一天刮大风，将花盆吹落到楼下，砸到了路过的行人，行人不治身亡。"
                "李四家住在32楼，李四将花盆丢下一楼，砸到了路过的行人，行人不治身亡。"
                "参考上述内容，请问张三和李四分别犯了什么罪，他们的判罪理由是什么，他们的量刑标准是什么？")
    # question = ("就是那个谁，张三，你告诉我张三的消息")
    # question = "光闸是什么"

    if test_all:
        rewrite_questions = rewrite_template.rewrite(question,model)
        print(rewrite_questions)
        knowledges = []
        for q in rewrite_questions:
            part = rank.topk(question=q, knowledge=knowledge,k=10)
            knowledges.append(part)
        # top_k = reduce(lambda item1,item2:item1 + item2,knowledges)

        top_k = rrf.topk(question=None,knowledge=knowledges,k=10)
        top_k = rerank.topk(question=question, knowledge=top_k,k=5)
        print(top_k)
        
        content = "".join(f"[详细内容：{value.source['path']} 子段：第{value.source['part']}部分]:\n{value.meta}\n" 
                          for value in top_k)
            
        prompt = template.apply(question,content)

        now_response, history = model.chat(prompt, history=None)

        print(now_response)
        print("*"*100)
    else:
        top_k = rank.topk(question=question, knowledge=knowledge, k=10)
        top_k = rerank.topk(question=question, knowledge=top_k,k=5)
        print(top_k)
        content = "".join(f"[详细内容：{value.source['path']} 子段：第{value.source['part']}部分]:\n{value.meta}\n"
                          for value in top_k)
        prompt = template.apply(question, content)
        now_response, history = model.chat(prompt, history=None)

        print(now_response)
        print("*"*100)