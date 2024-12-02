import json

from llm.base import BaseChatModel
import dashscope
from config import qwen_api_key


class Qwen(BaseChatModel):
    MODEL_NAME = "qwen"

    def __init__(self, version="qwen-plus"):
        self.version = version

    def apply_chat_template(self, prompt, history, role_prompt):
        if not role_prompt:
            role_prompt = "You are a helpful assistant."
        if not history:
            messages = [
                {"role": "system", "content": role_prompt},
                {"role": "user", "content": prompt}
            ]
        else:
            messages = history + [{"role": "user", "content": prompt}]
        return messages

    def stream_chat(self, prompt, history, role_prompt=None,
                    only_content=True):
        """
        流式对话接口
        
        Args:
            prompt (str): 用户输入的提示语
            history (list): 对话历史记录
            role_prompt (str, optional): 角色设定提示语. Defaults to None.
            
        Yields:
            response: 流式生成的回复内容
            
        Example:
            >>> qwen = Qwen(version="qwen-plus")
            >>> prompt = "你好"
            >>> history = []
            >>> for response in qwen.stream_chat(prompt, history):
            ...     print(response)
        """
        messages = self.apply_chat_template(prompt, history, role_prompt)

        responses = dashscope.Generation.call(
            api_key=qwen_api_key,
            model=self.version,
            messages=messages,
            result_format='message',
            stream=True,
            incremental_output=True
        )
        for response in responses:
            if only_content:
                role, response = self._parse_content(response=response)
                yield response

    def chat(self, prompt, history, role_prompt=None, only_content=True):
        messages = self.apply_chat_template(prompt, history, role_prompt)
        response = dashscope.Generation.call(
            api_key=qwen_api_key,
            model=self.version,
            messages=messages,
            result_format='message'
        )

        response = self._parse_content(response) if only_content else response
        return response

    def _parse_content(self, response):
        content = json.loads(str(response))
        output = content['output']['choices'][0]['message']
        role = output['role']
        response = output['content']
        return role, response
