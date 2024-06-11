from dataclasses import dataclass
from dataclasses import dataclass, fields
import json

@dataclass
class PromptTemplateRewriterSubq:
    role:str = ""
    purpose:str = ("你需要根据用户提供的问题进行问题的重写，以提供更好的搜索查询来回答给定问题。")
    skill: str = ""
    constraint:str = ("你需要充分理解用户问题，"
                      "以json格式返回重写后的问题。如果涉及多个问题，则将其分解成多个子问题。")
    few_shot:str = ("返回的单个问题json格式例子如下：```json\n[\n{\"question\":""}\n]\n```"+
                    "返回的多个问题json格式例子如下：```json\n[\n{\"question\":""},\n{\"question\":""}\n]\n```")
    question:str = "用户问题如下:"

    def apply(self,question):
        new_prompt = ""
        for field in fields(self):
            field_name = field.name
            field_value = getattr(self, field_name)
            if field_name =="question":
                new_prompt = new_prompt +field_value+ question + "\n"
                continue
            new_prompt = new_prompt + field_value + "\n"
        return new_prompt

    def rewrite(self,question, model):
        template = self.apply(question)
        response, _ = model.chat(template, None)
        parse_response = self.parse(response)+[question]
        return question if not parse_response else parse_response

    def parse(self,response):
        questions = []
        try:
            response = response.strip("```json\n").strip("\n```")
            data = json.loads(response)
            for item in data:
                questions.append(item['question'])
            return questions
        except json.decoder.JSONDecodeError as e:
            print(e)
            print("warning: rewrite fail!")
            return None


