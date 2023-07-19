import streamlit as st
import generate as gr
import tempfile

st.title('Generate a cover letter based on your C.V.')

uf = st.file_uploader("Choose a PDF file", type="pdf",key="pdf_reader")

if uf is not None:
    pdf_bytes = uf
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(pdf_bytes.getvalue())
        tmp_file_path = tmp_file.name
    index = gr.get_index(tmp_file_path)
    letter =  gr.generate_cover_letter(index)
    st.write(letter)