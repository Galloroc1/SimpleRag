from rag.fileQA.base import MetaData,Document
from dataclasses import dataclass, fields

@dataclass
class PromptTemplate:
    role:str = ("# 角色\n"
                "你是一个能够根据给定的参考资料回答问题的知识助手。")
    purpose:str = ("# 期望\n"
                   "你旨在根据用户提供的参考资料，帮助用户回答问题，返回问题答案。\n")
    skill: str = ("### 技能1:基于参考资料的问题解答\n"
                  "- 根据用户提供的问题和参考资料，以问答形式返回答案。\n"
                  "- 如果用户提供的参考资料无法找到答案，使用AI技术自行生成答案。\n"
                  "### 技能2:返回参考路径\n"
                  "- 根据用户提供的参考路径，返回相应的参考路径信息。\n")

    constraint:str = ("## 约束："
                      "- 必须使用用户使用的语言。\n"
                      "- 根据用户提供的参考路径，在答案末尾返回对应参考路径信息。\n"
                      "- 如果用户提供的参考资料无法找到答案，答案末尾返回[AI生成]作为参考来源。\n")




    content:str = "参考资料:\n"
    knowledge : Document = None
    question:str = "请输出参考路径及子段"
    few_shot:str = ("## 示例问答：\n"
                    "答案：[你的回答]\n参考路径:[参考路径]\n")

def add_knowledge(new_prompt,knowledge):
    for index, value in enumerate(knowledge):
        new_prompt = (new_prompt +f"[详细内容：{value.source['path']} 子段：第{value.source['part']}部分]:\n{value.meta}\n")
    return new_prompt

def add_question(new_prompt,question):
    new_prompt = new_prompt + "这是用户的问题:"+question
    return new_prompt


def apply_prompt_template(prompt:PromptTemplate,question:str,knowledge:Document)->str:
    new_prompt = ""
    for field in fields(prompt):
        field_name = field.name
        field_value = getattr(prompt, field_name)

        if field_name == "knowledge":
            new_prompt = add_knowledge(new_prompt,knowledge)+"\n"
        elif field_name == "question":
            new_prompt = add_question(new_prompt,question)+field_value+"\n"
        else:
            new_prompt = new_prompt + field_value+"\n"

    return new_prompt

