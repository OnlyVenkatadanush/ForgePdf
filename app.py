import streamlit as st
from functions import pdf_info, pdf_split, pdf_merge, pdf_secure, pdf_fill_form
from PyPDF2 import PdfReader, PdfWriter
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="ForgePDF", page_icon="🔨", layout="wide")
st.title("ForgePDF")
st.caption("Shape. Slice. Secure. Your PDF, your forge.🔥📄🛠️")

# --- UPLOAD PDF ---
doc = st.file_uploader("Upload a PDF file", type=["pdf"], key="file_uploader")

# Initialize reader and password outside the conditional block
reader = None
password = None
decryption_successful = False

if doc is not None:
    try:
        doc_bytes = io.BytesIO(doc.read())
        reader = PdfReader(doc_bytes)

        if reader.is_encrypted:
            st.warning("🔐 PDF is encrypted.")
            password = st.text_input("Enter the password to decrypt the PDF", type="password")
            if password:
                try:
                    decryption_result = reader.decrypt(password)
                    if decryption_result == 1:
                        st.success(f"✅ Decryption successful.")
                        decryption_successful = True
                    elif decryption_result == 0:
                        st.error(f"❌ Wrong password.")
                        reader = None
                        password = None
                    elif decryption_result == 2:
                        st.info("ℹ️ Password might be the owner password, or the PDF has other restrictions. Basic viewing might be possible.")
                        decryption_successful = True # Treat as successful for basic operations
                    else:
                        st.error(f"❌ Decryption failed with code: {decryption_result}")
                        reader = None
                        password = None
                except Exception as e:
                    st.error(f"❌ Decryption error: {e}")
                    reader = None
                    password = None
        else:
            st.success("🔓 PDF is not encrypted.")
            decryption_successful = True

        # Display PDF info only if reader is successfully loaded (or considered usable after owner password)
        if reader and decryption_successful:
            st.write("### PDF Info:")
            st.write(pdf_info(doc_bytes, password))

    except Exception as e:
        st.error(f"Error reading PDF: {e}")

# --- SIDEBAR FOR OPERATIONS ---
with st.sidebar:
    if reader and decryption_successful:
        st.title("📂 Operations")
        operation = st.radio("Choose an action", ("Split PDF", "Merge PDF", "Secure PDF", "Fill PDF Form"))

        # --- SPLIT PDF OPERATION ---
        if operation == "Split PDF":
            st.write("## Split PDF")
            if reader:
                try:
                    total_pages = len(reader.pages)
                    start_page = st.number_input("Start Page", min_value=1, value=1, max_value=total_pages if total_pages > 0 else 1)
                    end_page = st.number_input("End Page", min_value=1, value=total_pages if total_pages > 0 else 1, max_value=total_pages if total_pages > 0 else 1)

                    if start_page > end_page:
                        st.error("⚠️ Start page must be <= End page.")
                    elif end_page > total_pages:
                        st.error(f"⚠️ End page cannot exceed total pages ({total_pages}).")
                    elif st.button("Split"):
                        pdf_split(doc_bytes, start_page, end_page)
                except Exception as e:
                    st.error(f"❌ Error accessing PDF pages for splitting: {e}")
            else:
                st.warning("Upload and (if needed) decrypt a PDF first.")

        # --- MERGE PDF OPERATION ---
        elif operation == "Merge PDF":
            st.write("## Merge PDF")
            files = st.file_uploader("Upload multiple PDFs", type=["pdf"], accept_multiple_files=True)
            if st.button("Merge") and files:
                st.success(f"Merging {len(files)} PDF files.")
                pdf_merge(files)
            elif not files:
                st.info("Please upload PDF files to merge.")

        # --- SECURE PDF OPERATION ---
        elif operation == "Secure PDF":
            st.write("## Secure PDF")
            option = st.radio("Choose:", ("Encrypt PDF", "Decrypt PDF"))
            new_password = st.text_input("Enter password", type="password")

            if new_password and st.button("Apply"):
                if doc_bytes:
                    if option == "Encrypt PDF":
                        pdf_secure(doc_bytes, new_password)
                    elif password:  # Only attempt decryption if a password was entered for the uploaded file
                        pdf_secure(doc_bytes, password, unsecure=True) # Pass None for new_password to just decrypt
                    else:
                        st.warning("Please enter the original password to decrypt.")
                else:
                    st.warning("Please upload a PDF file first.")

        # --- FILL PDF FORM OPERATION ---
        elif operation == "Fill PDF Form":
            st.write("## Fill PDF Form")
            json_data = st.text_area("Enter form data (in JSON format)")
            if st.button("Fill Form") and doc_bytes and json_data:
                pdf_fill_form(doc_bytes, json_data)
            elif not doc_bytes:
                st.warning("Please upload a PDF file first.")
            elif not json_data:
                st.info("Please enter the form data in JSON format.")

    else:
        st.sidebar.info("⬆️ Upload a PDF file to see available operations on non-encrypted or successfully accessed PDFs.")

# --- ABOUT SECTION ---
with st.expander("ℹ️ About ForgePDF"):
    st.write("ForgePDF lets you manipulate PDF files with power and simplicity.")
    st.markdown("""
    **Features:**
    - 🔍 View PDF information
    - ✂️ Split PDF pages
    - 🧩 Merge multiple PDFs
    - 🔐 Encrypt & Decrypt PDFs
    - 📝 Fill PDF forms
    """)