import os
import json
import tempfile
from PyPDF2 import PdfReader, PdfWriter
import streamlit as st

def pdf_info(doc, password=""):
    try:
        reader = PdfReader(doc)

        # Decrypt if encrypted
        if reader.is_encrypted:
            try:
                reader.decrypt(password)
            except Exception as e:
                st.error("❌ Incorrect password or decryption failed.")
                return

        # Basic file details
        st.write("📄 **File Information**")
        st.write(f"• **Pages**: {len(reader.pages)}")
        st.write(f"• **Size**: {doc.getbuffer().nbytes / 1024:.2f} KB")
        st.write(f"• **Encrypted**: {'✅ Yes' if reader.is_encrypted else '❌ No'}")

        # First page info
        first_page = reader.pages[0]
        st.write(f"• **Page Size**: {first_page.mediabox.width} × {first_page.mediabox.height} pts")

        # Metadata
        meta = reader.metadata
        st.write(f"• **Metadata**: {meta if meta else 'No metadata found'}")

        # Text Preview
        preview = first_page.extract_text()
        st.write("📝 **Preview (first 300 characters)**:")
        st.code(preview[:300] if preview else "No extractable text found.")

        # Form Fields
        fields = reader.get_fields()
        if fields:
            st.write("🧾 **Form Fields**:")
            for key in fields:
                st.write(f"- {key}")
        else:
            st.write("🧾 **Form Fields**: None")

    except Exception as e:
        st.error(f"⚠️ Failed to extract PDF info: {e}")


def pdf_split(doc, start_page, end_page):
    reader = PdfReader(doc)
    writer = PdfWriter()

    for i in range(start_page - 1, end_page):
        writer.add_page(reader.pages[i])

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        output_file = tmp_file.name
        writer.write(tmp_file)

    st.success("✅ PDF split successfully!")
    with open(output_file, "rb") as f:
        st.download_button(
            label="📥 Download Split PDF",
            data=f,
            file_name=f"split_{start_page}_{end_page}.pdf",
            mime="application/pdf"
        )
    os.remove(output_file)

def pdf_merge(files):
    writer = PdfWriter()
    for file in files:
        reader = PdfReader(file)
        for page in reader.pages:
            writer.add_page(page)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        output_file = tmp_file.name
        writer.write(tmp_file)

    st.success("✅ PDFs merged successfully!")
    with open(output_file, "rb") as f:
        st.download_button(
            label="📥 Download Merged PDF",
            data=f,
            file_name="merged.pdf",
            mime="application/pdf"
        )
    os.remove(output_file)

def pdf_secure(doc, password, unsecure=False):
    reader = PdfReader(doc)
    if reader.is_encrypted and unsecure:
        try:
            reader.decrypt(password)
        except:
            st.error("❌ Wrong password.")
            return

    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    if not unsecure:
        writer.encrypt(password)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        output_file = tmp_file.name
        writer.write(tmp_file)

    st.success("✅ PDF encryption/decryption successful!")
    with open(output_file, "rb") as f:
        file_label = "decrypted" if unsecure else "encrypted"
        st.download_button(
            label=f"📥 Download {file_label.capitalize()} PDF",
            data=f,
            file_name=f"{file_label}.pdf",
            mime="application/pdf"
        )
    os.remove(output_file)

def pdf_fill_form(doc, form_data):
    try:
        form_data_dict = json.loads(form_data)
    except:
        st.error("❌ Invalid JSON format.")
        return

    reader = PdfReader(doc)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Fill form on all pages if needed
    for i, page in enumerate(reader.pages):
        writer.update_page_form_field_values(writer.pages[i], form_data_dict)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        output_file = tmp_file.name
        writer.write(tmp_file)

    st.success("✅ Form fields filled successfully!")
    with open(output_file, "rb") as f:
        st.download_button(
            label="📥 Download Filled PDF",
            data=f,
            file_name="filled_form.pdf",
            mime="application/pdf"
        )
    os.remove(output_file)
