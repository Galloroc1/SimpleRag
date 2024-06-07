import streamlit as st
import os
import sys
from pathlib import Path
root_path = str(Path.cwd().parents[0])
sys.path.append(root_path)
from rag.fileQA.loader.file_loader import TxtLoader,DocxLoader
from rag.fileQA.text_splitter.splitter import CharacterSplitter
from rag.fileQA.rerank.rerank import RerankerBge
from rag.fileQA.rank import RankEmbedding
from rag.fileQA.base import Document
from rich import  print
from rag.models.nlp.LLM.api import QwenApi
from rag.fileQA.template import PromptTemplateRAG,apply_prompt_template,PromptTemplateBase
import tempfile

def read_file(question,uploaded_file):
    loader_dict={
        "txt":TxtLoader,
        "docx":DocxLoader
    }
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    # todo: 随便写的 后续再改
    filetype = uploaded_file.name.split(".")[-1]
    data_loader = loader_dict[filetype](temp_file_path)
    data: Document = data_loader.load()

    os.remove(temp_file_path)

    spliter = CharacterSplitter(chunk_size=2000)
    knowledge: Document = spliter.split_document(data)

    # rank get top 20
    knowledge = st.session_state.rank.topk(question=question, knowledge=knowledge, k=20)

    # rerank get top 3
    top_k: Document = st.session_state.rerank.topk(question=question, knowledge=knowledge, k=3)
    # template = apply_prompt_template(prompt=PromptTemplate(), question=question, knowledge=top_k)

    template = apply_prompt_template(prompt=PromptTemplateBase(), question=question, knowledge=top_k)
    return template

def main():
    if 'model' not in st.session_state:
        print("init model")
        st.session_state.model = QwenApi()
    if 'rank' not in st.session_state:
        print("init rank")
        st.session_state.rank = RankEmbedding()
    if 'rerank' not in st.session_state:
        print("init rerank")
        st.session_state.rerank = RerankerBge()
    st.title("simple rag")

    with st.sidebar:
        uploaded_file = st.file_uploader(label="upload your file")

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
        if uploaded_file is not None:
            template = read_file(prompt,uploaded_file)
            response, _ = st.session_state.model.chat(template,history=st.session_state.messages)
        else:
            response, _ = st.session_state.model.chat(prompt, history=st.session_state.messages)

        with st.chat_message("system"):
            st.markdown(response)
        st.session_state.messages.append({"role": "system", "content": response})
if __name__ == '__main__':
    main()

