import random
import os
from config import api_key
os.environ['DASHSCOPE_API_KEY'] = api_key

from http import HTTPStatus
from dashscope import Generation
from llm.base import BaseChatModel


class QwenApi(BaseChatModel):

    def __init__(self,model_name="qwen-turbo"):
        self.model_name = model_name

    def chat(self,prompt,history):
        if not history:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        else:
            messages = history+[{"role": "user", "content": prompt}]
        response = Generation.call(model=self.model_name,
                                   messages=messages,
                                   # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
                                   seed=random.randint(1, 10000),
                                   # 将输出设置为"message"格式
                                   result_format='message')
        output_text = response.output.choices[0]['message']['content']
        new_history = messages + [{"role": "system", "content": output_text}]
        if response.status_code == HTTPStatus.OK:
            return output_text,new_history
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))


    def apply_chat_template(self,**kwargs):
        pass


    def stream_chat(self,prompt,history):
        """
        todo: should return history
        :param prompt:
        :param history:
        :return:
        """
        if not history:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        else:
            messages = history+[{"role": "user", "content": prompt}]


        responses = Generation.call(model="qwen-turbo",
                                    messages=messages,
                                    result_format='message',  # 设置输出为'message'格式
                                    stream=True,  # 设置输出方式为流式输出
                                    incremental_output=True  # 增量式流式输出
                                    )
        for response in responses:
            if response.status_code == HTTPStatus.OK:
                yield response.output.choices[0]['message']['content']
                # print(response.output.choices[0]['message']['content'], end='')
            else:
                print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                    response.request_id, response.status_code,
                    response.code, response.message
                ))

