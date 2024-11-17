from agent_core.tools.base import BaseTools
from typing import Dict, Optional, Union, List
from agent_core.schema import Params, Messages, SystemErrorInformation


class BaseCode(BaseTools):
    tool_description = "python执行器，主要用以执行某些具体的python代码"
    input_description: Optional[Dict] = {
        "code": Params(description="生成的python代码", dtype=str, is_must=True, default="")
    }

    output_description: Union[List[Dict], Dict] = {
        "result": Params(description="python代码执行的结果，结果变量以result存储",
                          dtype=str, is_must=False)
    }

    def action(self, params: Union[Dict, None] = None) -> Union[Dict, SystemErrorInformation, List[Dict]]:
        # todo: it's not safety, should run the code in docker
        exec_environment = {}
        try:
            exec(params["code"], exec_environment)
            result = exec_environment.get("result",
                                      "No result returned from the executed code.")
            return {"result": result}
        except Exception as e:
            return SystemErrorInformation(error_messages={"dtype": str(type(e).__name__),
                                                          "reason": str(e)})

if __name__ == '__main__':

    code = \
"""
import numpy as np

data1 = np.random.random_sample((3,3))
data2 = np.random.random_sample((3,3))

result = np.dot(data1,data2)
# print(result)
"""

    tool = BaseCode()
    data = tool.call({"code":code})
    print(data['result'])
