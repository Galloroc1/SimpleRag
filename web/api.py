import os
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse,Response
import torch
import sys
sys.path.append("/home/hr/pyproject/chatdoc")
from fastapi import FastAPI, Request

app = FastAPI()


@app.post("/chat/")
async def chat(request: Request):
    data = await request.json()
    history= data.get("history")
    question = data.get("question")
    file = data.get("file")
    headers = {"content-type":"text/event-stream"}
    try:
       return StreamingResponse(fix_res(responses), headers=headers)
    finally:
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()

