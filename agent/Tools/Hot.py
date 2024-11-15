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
    tool = AllHot()
    result = tool.call({'name':'百度'})
    print(f"result:{result}")

