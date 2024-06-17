from abc import ABC,abstractmethod
from pathlib import Path
root_path = str(Path.cwd().parents[2])
import sys
sys.path.append(root_path)
import os
from typing import List
import json5 as json
import re
import io
import contextlib

TOOL_REGISTRY = {}


def register_tool(name, allow_overwrite=False):
    pass


class BaseTools:
    name = "base tools"
    description = "base tools"
    parameters = "nothing"
    args_format = "nothing"


class ExampleTouchTools(BaseTools):
    function_name = 'ExampleTouchTools'
    name = "本地文件写入工具"
    description = "本地文件写入工具，输入文件路径和写入内容，返回写入状态True或者False"


    def run(self,path,file_name,content):
        try:
            if not os.path.exists(path):
                os.mkdir(path)
            file_path = os.path.join(path,file_name)
            if os.path.exists(file_path):
                os.remove(file_path)

            with open(file_path,'w') as f:
                f.write(content)
            return True
        except:
            return False


class ExampleCaluateTools(BaseTools):
    function_name = 'ExampleCaluateTools'
    name = "numpy矩阵计算器"
    description = "计算器，输入要计算的内容，返回计算结果"
    prompt = ("根据用户需求，使用numpy计算用户需求"
              "要求以```python\nxxxx\n```格式输出\n")

    def run(self,question,model):
        prompt = self.prompt + question
        code_str = self.parse_code(prompt,model)
        # print(code_str)
        output_buffer = io.StringIO()

        # 使用 contextlib.redirect_stdout 重定向输出到缓冲区
        with contextlib.redirect_stdout(output_buffer):
            exec(code_str)
        output = output_buffer.getvalue()
        # return code_str,output
        prompt = "参考代码和控制台的打印结果回答用户问题，代码及打印结果如下"+code_str+"\n"+output+"\n"+"用户问题如下"+question

        response,_ = model.chat(prompt,history=None)
        return response

    def parse_code(self,question,model):
        response,_ = model.chat(question,history=None)
        try:
            pattern = r"```python\n(.*?)\n```"
            response = re.findall(pattern, response, re.DOTALL)[0]
            print(response)
            print("*"*100)
            return response
        except json.decoder.JSONDecodeError as e:
            print(e)
            print("warning: parse fail!")
            return None


class ToolsChoice:
    roel_prompt = "你现在根据用户的问题，帮助人类选择合适的工具执行。\n"
    tools_prompt = "你现在有如下工具可以选择。\n"
    response_prompt = '你需要以json格式返回你的选择，格式如下:```json\n{"函数名":"","名称":""}\n```\n'
    question_prompt = "用户问题如下"

    def run(self,question,tools,model):
        tools_information = self.make_tools_prompt(tools)
        prompt = self.roel_prompt + self.tools_prompt + tools_information +self.response_prompt+ self.question_prompt + question

        response,_ = model.chat(prompt,history=None)
        choice = self.parse_json(response)
        return choice

    def make_tools_prompt(self,tools:List[BaseTools]):
        prompt = ""
        for index,value in enumerate(tools):
            prompt = prompt + f'工具{index}:\n\t--名称:{value.name}\n\t--工具描述:{value.description}\n\t--函数名:{value.function_name}\n'
        return prompt

    def parse_json(self,response):
        try:
            pattern = r"```json\n(.*?)\n```"
            response = re.findall(pattern, response, re.DOTALL)[0]
            data = json.loads(response)
            return {"函数名":data['函数名'],"名称":data['名称']}
        except :
            print("warning: parse fail!")
            return None


if __name__ == '__main__':

    from rag.models.nlp.LLM.api import QwenApi
    question = "我有一个二维矩阵A：[[1,2],[3,4]]，A的每个元素(x,y)代表它在一个8*8的全0矩阵B上对应的(x,y)坐标值为1，输出B矩阵结果"
    print(question)
    model = QwenApi()
    tools = [ExampleTouchTools, ExampleCaluateTools]
    choice = ToolsChoice().run(question,tools,model)
    response = eval(choice['函数名'])().run(question,model)
    print(response)