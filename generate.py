import os
import streamlit as st
import pinecone
import string
import random
from langchain.llms import OpenAI
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Pinecone
from langchain.chains import LLMChain

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

def get_index(filename):
    # Initialising pinecone
    pine_cone_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
    print(pine_cone_name)
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    pinecone.init(
    api_key=st.secrets['PINECONE_API_KEY'],
    environment=st.secrets['PINECONE_ENV']
    )

    indexes = pinecone.list_indexes()
    if pine_cone_name in indexes:
        return Pinecone.from_existing_index(pine_cone_name,embeddings)

    pinecone.create_index(pine_cone_name, dimension=1536)
    loader = PyPDFLoader(filename)
    pages = loader.load_and_split()   

    return Pinecone.from_documents(pages, embeddings, index_name=pine_cone_name) 

def generate_cover_letter(index):
    prompt_template = """Use the context below to write a cover letter:
    Context: {context}
    Cover letter:"""
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context"])
    llm = OpenAI(temperature=0.1, verbose=True)
    chain = LLMChain(llm=llm, prompt=PROMPT)

    docs = index.similarity_search("Thethela", k=4)
    inputs = [{"context": doc.page_content} for doc in docs]  
    letter = chain.apply(inputs)

    return letter 