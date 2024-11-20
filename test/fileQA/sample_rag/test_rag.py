import os
os.environ['HF_ENDPOINT'] = "https://hf-mirror.com"

import sys
from pathlib import Path

current_path = str(Path(sys.path[0]).resolve().parents[2])
sys.path.append(current_path)
from rag.fileQA.loader.file_loader import TxtLoader, DocxLoader, PDFLoader
from rag.fileQA.text_splitter.splitter import CharacterSplitter
from rag.fileQA.rank import RankBM25
from rag.fileQA.base import Document
# from rich import  print
from llm.api import QwenApi


def get_answer(question, kl):
    template = ""
    for index, value in enumerate(kl):
        template = (template + f"参考资料{index}说明：[来源][{value.source['path']}中第{value.source['part']}部分]\n" +
                    f"详细内容：{value.meta}")

    template = (template + f"用户问题如下：{question}\n" +
                (f"请你根据用户问题和用户提供的参考资料回答问题，同时输出参考文件的来源，要求内容准确、不允许胡编乱造。"))
    model = QwenApi()
    now_response, _ = model.chat(template, history=None)
    return now_response


if __name__ == '__main__':
    # file_path = os.path.join(current_path, "samples", "刑法.docx")
    file_path = os.path.join(current_path, "samples", "unet.pdf")
    file_type = os.path.splitext(file_path)[-1]
    file_class_dict = {'.txt': TxtLoader, '.docx': DocxLoader, '.pdf': PDFLoader}
    data = file_class_dict[file_type](file_path).load()
    print(f"data↓\n{data[0]}")

    # # data_loader = TxtLoader("/home/hr/pyproject/SampleRag/samples/天龙八部.txt")
    # data_loader = DocxLoader("/home/hr/pyproject/SampleRag/samples/刑法.docx")
    # data:Document = data_loader.load()

    spliter = CharacterSplitter(chunk_size=300)
    knowledge: Document = spliter.split_document(data)

    # question = ("2024年5月28日11时许，李小虎所报案称网上投资理财被骗数十万元。经查：李小虎2024年5月初在火炬路中房和园5号楼1单元6楼东家中，"
    #             "在网上学习炒股，后经自称客服人员引导，下载私域聊天软件，股票交易软件，通过炒股累计给对方提供的银行账号转账15万余元。请问这涉及什么案件")
    # question = "2024日5月28日11时许，建材路东路发生两辆电动车碰撞的事故，事故造成一人死亡，一人重伤。请问这是民事案件，还是刑事案件。"
    # question = "2024日5月28日11时许，王某自诉今天被丈夫打到浑身青紫。请问这个案件是否有转换成刑事案件的可能，请输出0到1之间的概率？"
    question = "what is unet"
    print(f'question{question}')
    # rank = RankEmbedding()
    rank = RankBM25()  # 暂时用
    # knowledge = rank.topk(question=question, knowledge=knowledge, k=20)
    top_k = rank.topk(question=question, knowledge=knowledge, k=5)
    # rerank = RerankerBge()    # 重排，暂时不用，下不了模型
    # top_k = rerank.topk(question=question, knowledge=knowledge, k=3)
    for i, v in enumerate(top_k):
        print(f"{i}->{v}")
    response = get_answer(question, top_k)
    print(f"response->{response}")
