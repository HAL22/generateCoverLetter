import streamlit as st
import generate as gr
import tempfile

st.title('Generate a cover letter based on your C.V.')

with st.form("my-form", clear_on_submit=True):
    file = st.file_uploader("Choose a PDF file", type="pdf",key="pdf_reader")
    name = st.text_input("Enter your name","",key="1")
    submitted = st.form_submit_button("Generate")
    
    if submitted and file is not None and name:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(file.getvalue())
            tmp_file_path = tmp_file.name
        index = gr.get_index(tmp_file_path)
        letter =  gr.generate_cover_letter(index)
        st.write(letter)        
