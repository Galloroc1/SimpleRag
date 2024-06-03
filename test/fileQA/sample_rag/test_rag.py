import os
import sys
sys.path.append("/home/hr/pyproject/SampleRag/")
from rag.fileQA.loader.file_loader import TxtLoader
from rag.fileQA.text_splitter.splitter import CharacterSplitter
from rag.fileQA.embedding.embedding import EmbeddingBgeM3
from rich import print
import numpy as np
from rag.models.nlp.LLM.api import QwenApi


def test_text_loader(path):
    data = TxtLoader(path).load()
    data = CharacterSplitter().split_document(data)
    return data

def get_max_scores_index(question,knowledge):
    embedding = EmbeddingBgeM3()

    knowledge_embeddings = embedding.encode_document(knowledge)
    question_embeddings = embedding.encode(question)

    cos_scores = knowledge_embeddings@question_embeddings.T
    max_args = np.argmax(cos_scores)
    return max_args

def get_answer(question,kl):
    template = (f"请你根据用户问题和用户提供的参考资料回答问题，同时输出参考文件的来源，要求内容准确、不允许胡编乱造。"
                f"限制：如果用户提供的资料不具备参考意义，你可以不必参考，但是需要给用户说明，说明语为：您的参考资料似乎跟问题无关。"
                +f"用户的参考资料如下:\n{str(kl.meta)}\n"
                +f"参考来源：路径{kl.source['path']}、"
                +f"part:{kl.source['part']}\n"
                +f"其中用户的问题如下:\n{question[0]}"
                )
    model = QwenApi()
    now_response, _ = model.chat(template, history=None)
    return now_response

if __name__ == '__main__':
    knowledge =  test_text_loader("/home/hr/pyproject/SampleRag/samples/天龙八部.txt")
    question = ["天龙八部中的龙指什么?"]
    max_args = get_max_scores_index(question,knowledge)
    must_like_sentences = knowledge[max_args]
    # print(must_like_sentences)
    print("*"*10)
    print("question",question[0])
    now_response = get_answer(question,must_like_sentences)
    print(now_response)
