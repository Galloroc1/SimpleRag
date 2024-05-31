import os
import sys
current_path = os.getcwd()
root_path = current_path[:current_path.find('rag')]+"rag"
sys.path.append(root_path)
from vllm import LLM,SamplingParams
from vllm.engine.llm_engine import LLMEngine
from config import cache_path
from transformers import AutoModelForCausalLM, AutoTokenizer


def test_Qwen1_5_vllm():
    llm = LLM(model="Qwen/Qwen1.5-32B-Chat-AWQ",download_dir=cache_path)
    prompts = [
        "Hello, my name is",
    ]
    sampling_params = SamplingParams(temperature=0.8, top_p=0.95)
    outputs = llm.generate(prompts, sampling_params)

    # Print the outputs.
    for output in outputs:
        prompt = output.prompt
        generated_text = output.outputs[0].text
        print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")

def test_Qwen1_5_hf():
    device = "cuda"  # the device to load the model onto
    model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen1.5-32B-Chat-GPTQ-Int4",
        torch_dtype="auto",
        device_map="auto",
        cache_dir=cache_path,
    )
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen1.5-32B-Chat-GPTQ-Int4",cache_dir=cache_path)

    prompt = "Give me a short introduction to large language model."
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    generated_ids = model.generate(
        model_inputs.input_ids,
        max_new_tokens=512
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(response)


if __name__ == '__main__':
    test_Qwen1_5_hf()