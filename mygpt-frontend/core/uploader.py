# /frontend/core/uploader.py

import streamlit as st


def upload_file():
    """
    Allows user to upload a PDF or CSV file and returns the file object.
    """
    st.subheader("📄 Upload Your Document")

    # File uploader component in Streamlit
    uploaded_file = st.file_uploader(
        label="Choose a PDF or CSV file to upload",
        type=["pdf", "csv"],
        help="Supported formats: .pdf or .csv only",
    )

    # If a file was uploaded, show a success message and return it
    if uploaded_file is not None:
        st.success(f"✅ '{uploaded_file.name}' uploaded successfully!")
        return uploaded_file

    # If nothing is uploaded, return None
    return None
