# ForgePdf
🔥 ForgePDF – Shape. Slice. Secure.
<h1 align="center">🛠️ ForgePDF</h1>
<p align="center">
  <img src="https://img.shields.io/badge/status-in%20progress-yellow?style=flat-square" />
  <img src="https://img.shields.io/badge/Built%20With-Streamlit-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/PDF%20Engine-PyPDF2-blue?style=flat-square" />
</p>

<p align="center">
  <img src="https://cdn-icons-png.flaticon.com/512/1226/1226858.png" width="120" alt="Hammer Logo" />
</p>

<h3 align="center">🔥 Shape. Slice. Secure. </h3>
<p align="center">Your PDF, your forge — built for clarity, control, and creativity.</p>

<p align="center">
  <a href="https://forgepdf.streamlit.app/" target="_blank">
    <img src="https://img.shields.io/badge/Launch%20App-Click%20Here-critical?style=for-the-badge&logo=streamlit&logoColor=white" />
  </a>
  &nbsp;
  <a href="https://github.com/YourUsername/ForgePDF" target="_blank">
    <img src="https://img.shields.io/badge/GitHub-Repo-333?style=for-the-badge&logo=github" />
  </a>
</p>

---

## ✨ Features

- **📄 PDF Info Viewer** — Instantly read and display metadata and page counts, even from encrypted PDFs.
- **✂️ PDF Splitter** — Select page ranges and extract content from PDFs with a single click.
- **🧩 PDF Merger** — Combine multiple PDFs into one seamless document.
- **🔐 Secure PDFs** — Encrypt or decrypt files on the fly using user-supplied passwords.
- **📝 PDF Form Filler** — Fill out PDF forms using clean JSON inputs.
- **🔒 Password Support** — Secure handling of password-protected files with inline decryption.

---

## 🚀 How to Use

1. **Launch the app** → [ForgePDF on Streamlit](https://forgepdf.streamlit.app/)
2. **Upload a PDF** → Or multiple, depending on your operation.
3. **Choose your operation** from the sidebar:
   - Split
   - Merge
   - Encrypt/Decrypt
   - Fill Form
4. **Interact with a clean, intuitive UI** → All operations are real-time and password-safe.
5. **Download your forged file** → Just like that.

---

## 🛠️ Tech Stack

| Tool        | Description                                |
|-------------|--------------------------------------------|
| **Streamlit** | Frontend UI and deployment platform     |
| **PyPDF2**     | Core PDF processing engine             |
| **Python**     | Backend logic and custom PDF handling |
| **io.BytesIO** | Efficient in-memory file processing    |

---

## ⚙️ Local Setup

```bash
# Clone the repo
git clone https://github.com/YourUsername/ForgePDF.git
cd ForgePDF

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
