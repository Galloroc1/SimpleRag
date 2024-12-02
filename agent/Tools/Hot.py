from operator import itemgetter

import requests
from agent_core.schema import SystemErrorInformation
from agent_core.tools.base import BaseTools
from agent_core.schema import Params
from typing import *
baidu_hot_url = "https://cn.apihz.cn/api/xinwen/baidu.php"
baidu_hot_params = {
    "id": "88888888",
    "key": "88888888"
}

all_hot_url = {'百度': {'url': baidu_hot_url, "params": baidu_hot_params},
       "sogou": {'url': baidu_hot_url, "params": baidu_hot_params}}

class AllHot(BaseTools):
    tool_description = '获取指定网站的热搜榜'
    input_description: Dict = {'name':Params(description="网站名", dtype=str, is_must=True, default='百度')}
    output_description = [{'quary':Params(description='标题', dtype=str, is_must=False),
                           'desc':Params(description='描述', dtype=str, is_must=False),
                           'url':Params(description='url', dtype=str, is_must=False)}]

    def action(self, params: Union[Dict, None] = None) -> Union[Dict, SystemErrorInformation, List[Dict]]:
        name = params['name']
        if name not in all_hot_url:
            return SystemErrorInformation(error_messages={'dtype': 'KeyError',
                                                          'reason': f"{name} not in {list(all_hot_url.keys())}" })
        data = requests.post(url=all_hot_url[name]['url'], data=all_hot_url[name]['params'])

        if data.status_code != 200:
            return SystemErrorInformation(error_messages={"dtype": "Network",
                                                          "reason": data.text})
        keys = ['query', 'desc', 'url']
        org_data = data.json()['data']
        print(f"org_data{org_data[0].keys()}")
        result = [dict(zip(keys, itemgetter(*keys)(x))) for x in org_data]
        return result

if __name__ == '__main__':
    """
    调用Qwen，判断用户问题对应的检索器类别
    """
    from LLM.qwen import Qwen
    user_question = '百度'
    # prompt = (f'请你根据用户的问题："{user_question}"，来判断这个问题是属于哪个热搜榜检索器，【百度，阿里，通义千问，其他】，'
    #           f'请以json的格式返回对应的结果,json格式为{{"type":"某检索器名称"}}, json的ensure_ascii=False')

    # prompt = (f'请你根据用户的问题："{user_question}"，来判断这个问题是属于哪个热搜榜检索器，检索器类别包括：【百度，阿里，通义千问，其他】，'
    #           f'只返回检索器的名称，不要返回其他内容')

    prompt = (f"你是一个智能助手，能够根据用户的问题判断其属于哪个热搜榜检索器，并返回相应的检索器名称。你的功能是判断检索器类别，"
              f"1）当用户提出一个问题时，根据问题内容判断其属于以下哪种热搜榜检索器：百度，阿里，通义千问，其他，"
              f"2）用户的问题必须是和检索器的热搜榜相关，而不是和某些概念相关，"
              f"3）只返回检索器的名称，不要返回其他内容。"
              f"注意：1）只讨论与热搜榜检索器相关的内容，拒绝回答与此无关的话题。2）输出内容必须仅包含检索器的名称，不要包含多余的信息或解释。"
              f"现在用户的问题是{user_question}，请你回答")
    print(prompt)
    history=[]
    role_prompt = '你是一个能判断哪个热搜榜的机器'
    qwen = Qwen(version="qwen-plus")
    response = qwen.chat(prompt=prompt, history=history, role_prompt=role_prompt, only_content=True)
    print(f"response:{response}")
    """
    根据用户的检索器类别，调取对应的检索接口
    """
    response_tool = response[-1]
    print(f"response_tool{response_tool}")
    if response_tool in all_hot_url:
        tool = AllHot()
        result = tool.call({'name': response_tool})
        print(f"result:{result}")

