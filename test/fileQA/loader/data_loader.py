import os
import sys
from pathlib import Path

from rag.models.nlp.LLM.api import QwenApi

current_path = str(Path(sys.path[0]).resolve().parents[2])
sys.path.append(current_path)
from rag.fileQA.loader.file_loader import TxtLoader,DocxLoader, PDFLoader


if __name__ == '__main__':
    # file_path = os.path.join(current_path, 'samples', '天龙八部.txt')
    # file_path = os.path.join(current_path,"samples","刑法.docx")
    file_path = os.path.join(current_path,"samples", "unet.pdf")
    file_type = os.path.splitext(file_path)[-1]
    file_class_dict = {'.txt': TxtLoader, '.docx': DocxLoader, '.pdf':PDFLoader}
    sentence = file_class_dict[file_type](file_path).load()
    print(f"sentence↓\n{sentence[0]}")

    # save_path = os.path.join(sys.path[0],"result")
    # os.makedirs(save_path,exist_ok=True)
    # PDFLoader(file_path)._save_load_page(save_path=save_path)
    # print(save_path)
