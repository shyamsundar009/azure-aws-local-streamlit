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
    with st.spinner("Azure blob storage contents are processing into chunks....."):
            for file_name in os.listdir("Azure_data"):
             pages.extend(load_file(f"Azure_data\\{file_name}"))
    shutil.rmtree("Azure_data")
    return pages
    
def azure_data_download(AZURE_CONNECTION_STRING,CONTAINER_NAME):
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    if not os.path.exists("Azure_data"):
        os.mkdir("Azure_data")
    for file_name in container_client.list_blobs():
        blob_client = container_client.get_blob_client(file_name)
        with open(f"Azure_data\\{file_name.name}", "wb") as file:
            data = blob_client.download_blob().readall()
            file.write(data)

st.sidebar.title("Azure Blob Storage Credentials")

# Input fields in sidebar
AZURE_CONNECTION_STRING = st.sidebar.text_input("Azure Connection String Input",type="password")
CONTAINER_NAME = st.sidebar.text_input("Azure Container Name")

st.title("Azure Blob Storage Data to Chroma Vector Database")

if st.sidebar.button("Injest"):
    # Check if all inputs are provided
    if AZURE_CONNECTION_STRING and CONTAINER_NAME:
        # Download PDF from Azure Blob Storage
        try:
            with st.spinner("Azure connection is creating....."):
                azure_data_download(AZURE_CONNECTION_STRING=AZURE_CONNECTION_STRING, CONTAINER_NAME=CONTAINER_NAME)
            pages = file_to_chunks()
            with st.spinner("Chroma VectorDatabse is creating....."):
                db = Chroma.from_documents(pages, OpenAIEmbeddings(), persist_directory="Chroma_db")
            st.success("Chroma VectorDatabse is created successfully")
        except Exception as e:
            st.error(f"Error downloading PDF: {str(e)}")
    else:
        st.warning("Please provide Azure Storage Account Name and Container Name.")
