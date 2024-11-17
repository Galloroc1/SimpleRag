from typing import List

from agent_core.schema import SystemErrorInformation
from agent_core.tools.base import BaseTools
from LLM.base import BaseChatModel
from typing import Dict, Union


CONTENT = """
# 角色
你是一个擅长任务规划的助手，能够合理利用手中资源为用户制定详细计划，并将任务拆分为一个个子任务。你会一步步思考，给出计划后暂停等待子任务的执行结果，用"pause"表示暂停。

## 技能
### 技能 1: 制定任务计划
1. 当用户提出需求时，仔细分析需求，确定需要完成的主要任务。
2. 将主要任务拆分为具体的子任务，并依次列出。
3. 对于每个子任务，评估所需资源，如 python 代码执行器、天气查询工具或热搜查询工具等。
4. 给出第一个子任务，并暂停等待执行结果。
===回复示例===
   - 子任务 1: <具体子任务描述>
   - 所需资源: <如果需要特定资源，列出资源名称>
   - pause
===示例结束===
5. 综合分析最终结果。执行完所有子任务之后，汇总结果报告给用户。
## 限制:
- 仅使用给定的资源进行任务规划和执行。
- 严格按照技能中的步骤进行操作，不得随意更改流程。
- 所输出的内容必须按照给定的格式进行组织，不能偏离框架要求。
"""


class Agent:
    description = "base agent"

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

    @property
    def _template(self):
        return ""

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


class LolAgent(Agent):
    description = "英雄联盟小助手,帮助用户提供英雄联盟的相应消息。"

    def __init__(self,
                 name,
                 llm,
                 input_description,
                 output_description,
                 tools):
        super().__init__(name,llm,input_description,output_description,tools)


class DotaAgent(Agent):
    description = "data小助手,帮助用户提供dota的相应消息。"

    def __init__(self,
                 name,
                 llm,
                 input_description,
                 output_description,
                 tools):
        super().__init__(name, llm, input_description, output_description, tools)


class GameAgent(Agent):
    description = "能够为用户提供网络游戏参考."
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

    def __init__(self):
        self.tools:List[Agent] = [GameAgent]


    def apply_template(self,query):
        # todo: bug here
        tools = "现有的工具如下".join(item.description+"希望输入:"+
                                      item.input_description+"希望输出："+
                                      item.output_description
                                      for item in self.tools)
        content = CONTENT+tools+query
        return content

    def test_chat(self,content,add_value=0):
        # 此处模拟model输出
        if not add_value:
            data = """
            首先我们分析这属于游戏助手的内容，我们直接捕获游戏助手返回的内容即可。
            - 子任务1：用户希望英雄里面现版本最强的上单top3
            - 工具：GameAgent
            - 输入:[无]
            - parse
            """
        elif add_value==1:
            data = """
            当前子任务执行结果为：[{'name':'剑圣','score':'52%'},
            {'name':'蛮王','score':'51%'},
            {'name':'赵信','score':'50%'}]
            """
        elif add_value==2:
            data = """
            当前版本最强top3上单为剑圣，胜率52%;蛮王，胜率51%;赵信，胜率50%.
            """
        elif add_value==3:
            data = """
            stop
            """

        for i in data:
            yield i

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
        query = "帮我查询英雄联盟里面现版本最强的上单top3"
        content = self.apply_template(query)
        all_response = ""
        add_value = 0

        while True:
            now_response = ""
            for i in self.test_chat(content,add_value):
                now_response = now_response + i
                yield i

            if self.check_stop(now_response):
                break

            tool, params = self.parse_params(now_response)
            # result not used here
            # result = self.action(tool, params)
            add_value = add_value + 1






if __name__ == '__main__':
    # game_agent = Task(name="tom",
    #                   llm=BaseChatModel,
    #                        input_description="帮助用户获取如下内容：英雄里面现版本最强的上单top5",
    #                        output_description="英雄联盟现版本最强的5个上单，"
    #                                           "包括中文名称和英文名称以及胜率")
    task = Task()
    result = task.call()
    for i in result:
        print(i,end="")