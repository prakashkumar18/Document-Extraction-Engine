import streamlit as st
import requests

# Deployed FastAPI backend
BACKEND_URL = "https://document-extraction-engine-6q2n.onrender.com"

st.title("AI Document Extraction Engine")

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

        try:
            response = requests.post(
                f"{BACKEND_URL}/extract",
                files=files,
                data=data
            )

            st.subheader("Extraction Result")

            try:
                st.json(response.json())

            except Exception:
                st.write(response.text)

        except requests.exceptions.RequestException as e:
            st.error(f"Unable to connect to backend: {e}")

    else:
        st.warning("Please upload a TXT or PDF file.")

st.subheader("Extraction History")

try:

    history = requests.get(
        f"{BACKEND_URL}/extractions"
    )

    st.json(history.json())

except requests.exceptions.RequestException:
    st.write("Unable to connect to backend.")
    )
