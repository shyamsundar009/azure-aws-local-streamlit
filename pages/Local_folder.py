import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from azure.storage.blob import BlobServiceClient
import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv  import load_dotenv
load_dotenv()
import shutil

def load_file(file_name):
    loader=[]
    print(file_name.split(".")[-1])
    if file_name.split('.')[-1] == "pptx":
        loader = UnstructuredPowerPointLoader(file_name).load()
    elif file_name.split('.')[-1] == "pdf":
        loader = PyPDFLoader(file_name).load()    
    elif file_name.split('.')[-1] == "docx":
        loader = Docx2txtLoader(file_name).load()
    elif file_name.split('.')[-1] == "html":
        loader = UnstructuredHTMLLoader(file_name).load()
    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=0,
            is_separator_regex=False,
        )
    pages = text_splitter.split_documents(loader)
    return pages

def file_to_chunks():
    pages=[]
    for file_name in os.listdir("local_data"):
        pages.extend(load_file(f"local_data\\{file_name}"))
    return pages
    

st.title("Local Data to Chroma Vector Database")

if st.button("Injest"):
    with st.spinner("Local Folder documents to chunks are in the process.........."):
        pages = file_to_chunks()
    with st.spinner("Chroma VectorDatabse is creating....."):
        db = Chroma.from_documents(pages, OpenAIEmbeddings(), persist_directory="Chroma_db")
    st.success("Chroma VectorDatabse is created successfully")