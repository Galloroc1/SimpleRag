
# vllm
cmd = ("python -m vllm.entrypoints.openai.api_server "
       "--served-model-name Qwen2-72B-Instruct-GPTQ-Int4 "
       "--model /home/hr/.cache/huggingface/hub/models--Qwen--Qwen2-72B-Instruct-GPTQ-Int4/snapshots/f712fd81df47a38f4d376ff19b843f6a4cfcb5fd "
       "--tensor-parallel-size 4")

