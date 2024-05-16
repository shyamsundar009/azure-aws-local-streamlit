import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import UnstructuredPowerPointLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import boto3
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
    with st.spinner("AWS S3 contents are processing into chunks....."):
        for file_name in os.listdir("S3_data"):
            pages.extend(load_file(f"S3_data\\{file_name}"))
    shutil.rmtree("S3_data")
    return pages
    
def aws(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET_NAME,object_name):
        # Create an S3 client
    s3 = boto3.client('s3',
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    # List objects in the bucket
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if not os.path.exists("S3_data"):
        os.mkdir("S3_data")

    # Download files in the 'data' object
    for i in response.get('Contents',[]):
        if i['Key'].split('/')[-1] != "" and i['Key'].split('/')[0] == object_name:
            # print(i['Key'])
            file_path = os.path.join("S3_data", i['Key'].split('/')[-1])
            # print(file_path)
            s3.download_file(BUCKET_NAME, i['Key'], file_path)

st.title("AWS S3 Data to Chroma Vector Database")

st.title("AWS S3 Credentials")

# Input fields in sidebar
aws_access_key = st.text_input("AWS Access Key",type="password")
aws_secret_access_key = st.text_input("AWS SECRET ACCESS KEY",type="password")
bucket_name= st.text_input("AWS BUCKET NAME")
object_name= st.text_input("AWS OBJECT NAME")

if st.button("Injest"):
    # Check if all inputs are provided
    if aws_access_key and aws_secret_access_key and bucket_name and object_name:
        # Download PDF from Azure Blob Storage
        try:
            with st.spinner("AWS connection is creating....."):
                aws(AWS_ACCESS_KEY_ID=aws_access_key, AWS_SECRET_ACCESS_KEY=aws_secret_access_key, BUCKET_NAME=bucket_name, object_name=object_name)
            pages = file_to_chunks()
            with st.spinner("Chroma VectorDatabse is creating....."):
                db = Chroma.from_documents(pages, OpenAIEmbeddings(), persist_directory="Chroma_db")
            st.success("Chroma VectorDatabse is created successfully")
        except Exception as e:
            st.error(f"Error in connecting with AWS: {str(e)}")
    else:
        st.warning("Please provide AWS CREDENTIALS.")
