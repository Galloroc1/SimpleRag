import os
import sys
from pathlib import Path
root_path = str(Path.cwd().parents[1])
sys.path.append(root_path)
from dataclasses import dataclass, fields
from rag.fileQA.template import PromptTemplate,apply_prompt_template
from rag.fileQA.base import MetaData,Document
if __name__ == '__main__':
    prompt = PromptTemplate()
    data = MetaData("你好!",source={"path":"now","part":"0"})
    data = Document([data])
    data = apply_prompt_template(prompt,question="你好",knowledge=data)
    print(data)