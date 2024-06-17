import sys
from pathlib import Path

current_path = str(Path(sys.path[0]).resolve().parents[1])
sys.path.append(current_path)
from rag.models.nlp.LLM.api import QwenApi

# from rich import print

if __name__ == '__main__':
    question = ("'第二百三十三条\u3000过失致人死亡的，处三年以上七年以下有期徒刑；情节较轻的，处三年以下有期徒刑。本法另有规定的，依照规定。\n第二百三十四条\u3000故意"
                "伤害他人身体的，处三年以下有期徒刑、拘役或者管制。\n犯前款罪，致人重伤的，处三年以上十年以下有期徒刑；致人死亡或者以特别残忍手段致人重伤造成严重残疾的，处)"
                "十年以上有期徒刑、无期徒刑或者死刑。本法另有规定的，依照规定。\n第二百三十四条之一\u3000组织他人出卖人体器官的，处五年以下有期徒刑，并处罚金；情节严重的，"
                "处五年以上有期刑，并处罚金或者没收财产。")
    model = QwenApi()
    now_response, history = model.chat(question+"请参考上述资料，提取多个问题"
                                                "严格按照json的形式返回结果，例如：'''json\n[{‘question’,‘question’}]", history=None)
    print(now_response)
    aaa,history = model.chat(question+"参考上述资料,回答下述问题，并且请你合理扩展，丰富回答。"+
                                      "过失致人死亡的法定刑罚是什么？",None)
    print(aaa)
