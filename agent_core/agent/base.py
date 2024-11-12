from typing import List

from agent_core.schema import SystemErrorInformation
from agent_core.tools.base import BaseTools


class Agent:

    def __init__(self, name):
        super().__init__()
        self.name = name

    def call(self):
        pass

    def plan(self):
        pass

    def react(self):
        pass


    def call(self, params: str):
        try:

            out_params = SystemErrorInformation({"dtype": "IndexError", "reason": "the chain of tools have no tool"})
            for tool in self.tools:
                out_params = tool.call(params)
                params = out_params
            return out_params
        except Exception as e:
            return SystemErrorInformation({"dtype": str(e.__class__.__name__), "reason": str(e)})
