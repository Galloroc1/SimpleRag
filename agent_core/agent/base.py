from typing import List
import sys
sys.path.append("/home/icaro/pyproject/SimpleRag")
import os
os.environ['DASHSCOPE_LOGGING_LEVEL'] = "info"
from agent_core.schema import SystemErrorInformation
from agent_core.tools.base import BaseTools
from llm.base import BaseChatModel
from typing import Dict, Union


CONTENT = """
# 角色
你是一个擅长任务规划的助手，能够合理利用手中工具或代理为用户制定详细计划。你会一步步思考，逐步给当前所需子任务并暂停等待子任务的执行结果.

首先判断历史内容和当前结果是否能够满足用户，如果是is_wait则为False，表明完成任务，无需等待，否则为True
然后思考当前步骤要做什么，给定purpose content。
然后需要使用哪些tool或agent，
最后以json格式返回结果。

返回示例：
思维链：<思考过程>
```json
{
    "is_wait":<is parse>,
    "purpose":<purpose content>
    "tool":<tool name>,
    "agent":<agent name>,
}

## 限制:
- 仅使用给定的工具或代理进行任务规划和执行。
- 严格按照技能中的步骤进行操作，不得随意更改流程。
- 所输出的内容必须按照给定的格式进行组织，不能偏离框架要求。
"""


class Agent:
    description = "base agent"
    input_description = ""
    output_description = ""
    def __init__(self, name,
                 llm,
                 input_description,
                 output_description,
                 tools):
        super().__init__()
        self.name = name
        self.llm:BaseChatModel = llm
        self.tools: Union[Agent, BaseTools] = tools
        self.input_description = input_description
        self.output_description = output_description

    def plan(self, plan_text=None):
        if not plan_text:
            pass
        else:
            return plan_text

    def react(self):
        pass

    def observe(self):
        pass

    def pause(self):
        pass

    def action(self):
        # 根据用户
        while True:
            for item in self.llm.stream_chat():
                content = ""

    def call(self, params: Dict):
        plan_text = self.plan()

    @classmethod
    def information(cls):
        strings = (f"name:{cls.__name__}\n description：{cls.description}\n"
                   f"输入期望：{cls.input_description}\n"
                   f"输出期望：{cls.output_description}\n")
        return strings

    def __str__(self):
        return self.information

class LolAgent(Agent):
    description = "英雄联盟小助手,帮助用户提供英雄联盟的相应消息。"

    def __init__(self,
                 name,
                 llm,
                 input_description,
                 output_description,
                 tools):
        super().__init__(name,llm,input_description,output_description,tools)


class WeatherAgent(Agent):
    description = "天气助手，查询今天天气"
    input_description = ""
    output_description = ""

    def __init__(self,
                 name,
                 llm,
                 tools,
                 input_description="用户需求",
                 output_description="需求结果",
                 ):
        super().__init__(name, llm, input_description, output_description, tools)


class GameAgent(Agent):
    description = "能够为用户提供所有的网络游戏参考"
    input_description = ""
    output_description = ""

    def __init__(self,
                 name,
                 llm,
                 tools,
                 input_description="用户需求",
                 output_description="需求结果"):
        super().__init__(name,llm,input_description,output_description,tools)


    def call(self, params: Union[Dict,None]):
        if not params:
            pass


class Task():

    def __init__(self,llm):
        self.tools:List = [GameAgent,WeatherAgent]
        self.llm = llm


    def apply_template(self,query):
        tools = "现有的代理如下:\n"+"".join(item.information() for item in self.tools)
        return tools


    def check_parse(self,response):
        return 'parse' in response

    def check_stop(self,response):
        return 'stop' in response

    def parse_params(self,response):
        return 'GameAgent',{}

    def action(self,agent,params):
        agent = eval(agent)
        result = agent.call(params)
        return result


    def call(self,query=None):
        content = self.apply_template(query)
        add_value = 0
        item = 0
        history = []
        while True:
            new_content = ""
            for i in self.llm.stream_chat(prompt=query,history=history,role_prompt=CONTENT+content):
                print(i,end="")
                new_content = new_content + i
            answer = input()
            history = history+[{"role":"user","content":query},
                               {"role":"system","content":new_content},
                               {"role":"user","content":answer}]
            print(history)
            # tool, params = self.parse_params(now_response)
            # result not used here
            # result = self.action(tool, params)
            # add_value = add_value + 1



if __name__ == '__main__':
    from llm.qwen import Qwen

    task = Task(llm=Qwen())
    query = input("please input your query")
    result = task.call(query)
    for i in result:
        print(i,end="")