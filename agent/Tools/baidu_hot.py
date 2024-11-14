import requests

from agent_core.tools.base import BaseTools
from typing import Dict, Optional, Union, List
from agent_core.schema import Params, Messages, SystemErrorInformation
import requests
from agent_core.schema import SystemErrorInformation

baidu_hot_url = "https://cn.apihz.cn/api/xinwen/baidu.php"
baidu_hot_params = {
    "id": "88888888",
    "key": "88888888"
}


class BaiduHot(BaseTools):
    tool_description = "用来捕获当日百度热搜榜"
    input_description: Optional[Dict] = None
    output_description: Union[List[Dict], Dict] = [{"query": Params(description="标题", dtype=str,
                                                                    is_must=False, default="None", param_range=[]),
                                                    "desc": Params(description="描述", dtype=str, is_must=False,
                                                                   default="None", param_range=[]),
                                                    "url": Params(description="原文地址", dtype=str, is_must=False,
                                                                  default="None", param_range=[])}]

    def action(self, params: Union[Dict, None] = None) -> Union[Dict, SystemErrorInformation, List[Dict]]:
        data = requests.post(url=baidu_hot_url, data=baidu_hot_params)
        if data.status_code != 200:
            return SystemErrorInformation(error_messages={"dtype": "Network",
                                                          "reason": data.text})
        keys = ['query', 'desc', 'url']
        org_data = data.json()['data']
        result = list(map(lambda x: {key: x[key] for key in keys}, org_data))
        return result


if __name__ == '__main__':
    tool = BaiduHot()
    data = tool.call()
    # print(data)
    data = Params(description="描述", dtype=str, is_must=False, default="None", param_range=[])
    print(data)
