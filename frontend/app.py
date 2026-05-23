import streamlit as st
import requests

st.title(
    "AI Document Extraction Engine"
)

uploaded_file = st.file_uploader(
    "Upload TXT or PDF File",
    type=["txt", "pdf"]
)

document_type = st.selectbox(
    "Select Document Type",
    ["invoice", "resume"]
)

if st.button("Extract"):

    if uploaded_file is not None:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type
            )
        }

        data = {
            "document_type": document_type
        }

        response = requests.post(
            "http://127.0.0.1:8000/extract",
            files=files,
            data=data
        )

        st.subheader(
            "Extraction Result"
        )

        try:

            st.json(
                response.json()
            )

        except:

            st.write(
                response.text
            )

st.subheader(
    "Extraction History"
)

try:

    history = requests.get(
        "http://127.0.0.1:8000/extractions"
    )

    st.json(history.json())

except:

    st.write(
        "Backend not running"
    )