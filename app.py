import streamlit as st
import requests

st.set_page_config(page_title="SumIt AI", layout="wide")

st.title("SumIt AI - PDF Summarizer")

uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])
question = st.text_input("Optional: What question do you want to focus on?")

if st.button("Summarize"):
    if uploaded_file is not None:
        # Prepare request to FastAPI
        files = {"file": uploaded_file.getvalue()}
        data = {"question": question} if question else {}

        with st.spinner("Summarizing..."):
            response = requests.post(
                "http://127.0.0.1:8000/summarize/",
                files={"file": (uploaded_file.name, uploaded_file, "application/pdf")},
                data=data
            )

        if response.status_code == 200:
            summary = response.json().get("summary", "No summary returned.")
            st.subheader("Summary:")
            st.text_area("Summary Text", summary, height=300)
        else:
            st.error(f"Error: {response.status_code}\n{response.text}")
    else:
        st.warning("Please upload a PDF file first.")
