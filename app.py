import streamlit as st
import generate as gr
import tempfile

st.title('Generate a cover letter based on your C.V.')

open_ai_key = st.text_input("Enter OpenAI API key", type="password")
pinecone_key = st.text_input("Enter Pinecone API key", type="password")
pinecone_env = st.text_input("Enter Pinecone Environment key")
gr.fill_keys(open_ai_key,pinecone_key,pinecone_env)

with st.form("generate-form", clear_on_submit=True):    
    file = st.file_uploader("Choose a PDF file", type="pdf",key="pdf_reader")
    name = st.text_input("Enter your name","",key="1")
    temp = st.slider("Choose the OpenAI temperature (creativity scale)",min_value=0.1, max_value=0.9, step=0.1)
    submitted = st.form_submit_button("Generate")
    
    if submitted and file is not None and name and open_ai_key and pinecone_key and pinecone_env :
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(file.getvalue())
            tmp_file_path = tmp_file.name
        index = gr.get_index(tmp_file_path)
        letter =  gr.generate_cover_letter(index,name,temp)
        st.write(letter)        