from typing import Union, Dict, List

from agent_core.schema import SystemErrorInformation
from agent_core.tools.base import BaseTools
from agent_core.schema import Params
from typing import *


class AllHot(BaseTools):
    tool_description = '获取指定网站的热搜榜'
    input_description: Dict = {'name':Params(description="网站名", dtype=str, is_must=True, default='百度')}
    output_description = [{'quary':Params(description='标题', dtype=str, is_must=False),
                           'desc':Params(description='描述', dtype=str, is_must=False),
                           'url':Params(description='url', dtype=str, is_must=False)}]

    url = {'百度':{'url':"a","params":"xxx"},
           "sogou":{}}

    def action(self, params: Union[Dict, None] = None) -> Union[Dict, SystemErrorInformation, List[Dict]]:
        name = params['name']
        if name not in self.url:
            return SystemErrorInformation(error_messages={'dtype': 'KeyError',
                                                          'reason': f"{name} not in {self.url}" })
        # return result
        # post name hot
        # return
        return {}

tool = AllHot()
data=tool.call({'name':'百度'})
print(data)

