from transformers import AutoModelForCausalLM, AutoTokenizer
from config import cache_path
from base import BaseChatModel


class Qwen(BaseChatModel):
    MODEL_NAME = "qwen"
    model = None
    tokenizer = None

    def __init__(self,device="cuda"):
        self.device = device

    def load_model(self):
        self.model = AutoModelForCausalLM.from_pretrained(
            "Qwen/Qwen1.5-32B-Chat",
            torch_dtype="auto",
            device_map="auto",
            cache_dir=cache_path,
        )
        self.tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen1.5-32B-Chat", cache_dir=cache_path)


    def chat(self,prompt,history):
        if not history:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        else:
            messages = history+[{"role": "user", "content": prompt}]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.device)

        generated_ids = self.model.generate(
            model_inputs.input_ids,
            max_new_tokens=512
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        new_history = messages + [{"role": "system", "content": response}]
        return response,new_history