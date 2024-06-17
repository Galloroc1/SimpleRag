import os
import sys
from pathlib import Path

from rag.models.nlp.LLM.api import QwenApi

current_path = str(Path(sys.path[0]).resolve().parents[2])
sys.path.append(current_path)
from rag.fileQA.loader.file_loader import TxtLoader,DocxLoader, PDFLoader

def get_answer(question,kl):
    template = (f"请你根据用户问题和用户提供的参考资料回答问题，同时输出参考文件的来源，要求内容准确、不允许胡编乱造。"
                f"限制：如果用户提供的资料不具备参考意义，你可以不必参考，但是需要给用户说明，说明语为：您的参考资料似乎跟问题无关。"
                +f"用户的参考资料如下:\n{str(kl.meta)}\n"
                +f"参考来源：路径{kl.source['path']}、"
                +f"其中用户的问题如下:\n{question}"
                )
    # print(template)
    model = QwenApi()
    now_response, _ = model.chat(template, history=None)
    return now_response

if __name__ == '__main__':
    # file_path = os.path.join(current_path, 'samples', '天龙八部.txt')
    # file_path = os.path.join(current_path,"samples","刑法.docx")
    file_path = os.path.join(current_path,"samples", "unet.pdf")
    file_type = os.path.splitext(file_path)[-1]
    file_class_dict = {'.txt': TxtLoader, '.docx': DocxLoader, '.pdf':PDFLoader}
    sentence = file_class_dict[file_type](file_path).load()
    print(f"sentence↓\n{sentence[0]}")

    # check

    # question = "刑法第一百零二条是什么"
    # now_response = get_answer(question, sentence[0])
    # print("question:", question)
    # print(now_response)
