from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import List, Dict, Union

from agent_core.schema import Params, Messages, SystemErrorInformation
from agent_core.tools.logger import logger

registered_tools = {}


class ToolMeta(type(ABC)):
    default_property = ['tool_description', 'input_description', 'output_description']
    """元类，用于自动注册工具"""

    def __new__(cls, name, bases, dct):
        new_cls = super().__new__(cls, name, bases, dct)
        if name != "BaseTools":
            has_property = list(filter(lambda x: x in new_cls.__dict__, cls.default_property))
            if len(has_property) == len(cls.default_property):
                registered_tools[name] = new_cls
                logger.info(f"[register tools]: register tool successfully, tool is:{name}")

            else:
                logger.error(f"[register tools]: register tool failed, reason: missing class properties")
                raise
        return new_cls


class BaseTools(ABC, metaclass=ToolMeta):
    """
    input_description and output_description just support json or List of Dict
    """
    tool_description: str = "default description"
    input_description: Union[Dict, List[Dict]] = {"default": "default"}
    output_description: Union[Dict, List[Dict]] = {"default": "default"}

    def assert_params(self, params: Dict, is_input_params: bool = True):
        # todo: may have some bug here
        description = self.input_description if is_input_params else self.output_description
        iters = description.items() if isinstance(description, dict) else description[0].items()
        params = params if isinstance(params, dict) else params[0]

        # value: Params
        for key, value in iters:
            # todo: check params dtype
            # check must
            print(value.is_must, value)
            print(key, params)
            if value.is_must and key not in params:
                return SystemErrorInformation(
                    error_messages={"dtype": "KeyError", "reason": f"key:{key} is must ,but not in params"})

            # check range，
            if value.param_range:
                if isinstance(params[key], Iterable):
                    for params_item in params[key]:
                        if params_item not in value.param_range:
                            SystemErrorInformation(error_messages={'dtype': 'RangeError',
                                                                   'reason': f'the param of {params_item} is invalid, '
                                                                             f'we just support f{value.param_range}'})
                else:
                    if params[key] not in value.param_range:
                        SystemErrorInformation(error_messages={'dtype': 'RangeError',
                                                               'reason': f'the param of {params[key]} is invalid, '
                                                                         f'we just support f{value.param_range}'})

            if not value.is_must:
                params.update({key: value.default})

        return params

    @abstractmethod
    def action(self, params: Union[Dict, None] = None) -> Union[Dict, SystemErrorInformation, List[Dict]]:
        raise NotImplementedError

    def call(self, params: Union[Dict, None] = None) -> Union[Messages, SystemErrorInformation, Dict]:
        if params:
            params = self.assert_params(params, is_input_params=True)
        if isinstance(params, SystemErrorInformation):
            return params

        try:
            output_result = self.action(params)
            if isinstance(output_result, SystemErrorInformation):
                return output_result

            return output_result
        except Exception as e:
            return SystemErrorInformation(error_messages={"dtype": str(type(e)), "reason": str(e)})

    def __str__(self):
        show_dicts = {
            "工具名": self.__class__.__name__,
            "描述": self.tool_description,
            "输入参数": self.input_description,
            "输出参数": self.output_description,
        }
        return str(show_dicts)


if __name__ == '__main__':
    value = registered_tools.values()
    print(value)
