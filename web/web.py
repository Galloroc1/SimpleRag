import streamlit as st
import os
import sys
from pathlib import Path
root_path = str(Path.cwd().parents[0])
sys.path.append(root_path)
from rag.fileQA.loader.file_loader import TxtLoader
from rag.fileQA.text_splitter.splitter import CharacterSplitter
from rag.fileQA.rerank.rerank import RerankerBge
from rag.fileQA.rank import RankEmbedding
from rag.fileQA.base import Document
from rich import  print
from rag.models.nlp.LLM.api import QwenApi
from rag.fileQA.template import PromptTemplate,apply_prompt_template
import tempfile

model = QwenApi()

st.title("simple rag")

with st.sidebar:
    uploaded_file = st.file_uploader(label="upload your file")
if uploaded_file:
    file_details = {
        "filename": uploaded_file.name,
        "filetype": uploaded_file.type,
        "filesize": uploaded_file.size
    }
    # st.write(file_details)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    data_loader = TxtLoader(temp_file_path)
    data: Document = data_loader.load()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    if uploaded_file:
        question = prompt
        spliter = CharacterSplitter(chunk_size=2000)
        knowledge: Document = spliter.split_document(data)

        # rank get top 20
        rank = RankEmbedding(question=question, knowledge=knowledge)
        rank.rank()
        knowledge = rank.topk(20)

        # rerank get top 3
        rerank = RerankerBge(question=question, knowledge=knowledge)
        rerank.rank()
        top_k: Document = rerank.topk(3)

        # apply prompt template
        template = apply_prompt_template(prompt=PromptTemplate(), question=question, knowledge=top_k)
        response,history = model.chat(template,history=None)
    else:
        response, history = model.chat(prompt, history=None)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

