import streamlit as st

def setup_page():
    st.set_page_config(page_title="Text Summarizer", layout="centered")

def render_header():
    st.title("Text Summarizer")
    st.caption("Aplikasi ini menggunakan model Llama-3.3-70b-versatile (via Groq).")

def render_form():
    """Merender elemen input sesuai urutan gambar yang diminta."""
    
    # 1. Text Input (Paling Atas)
    text_input = st.text_area("Masukkan teks di sini:", height=200, placeholder="Paste artikel atau teks panjang Anda di sini...")
    
    # 2. File Upload (Di bawah Text Input)
    st.write("Atau unggah file (.pdf)")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf", label_visibility="collapsed")
    
    # 3. Opsi (Bersebelahan / 2 Kolom)
    col1, col2 = st.columns(2)
    
    with col1:
        length_option = st.selectbox(
            "Pilih panjang ringkasan:",
            ("Pendek", "Sedang", "Panjang"),
            index=0
        )
    
    with col2:
        format_option = st.selectbox(
            "Format Output:",
            ("Terstruktur", "Formal", "Bullet Points"),
            index=0
        )
    
    # Mapping values untuk backend
    length_map = {"Pendek": "short", "Sedang": "medium", "Panjang": "long"}
    format_map = {"Terstruktur": "terstruktur", "Formal": "formal", "Bullet Points": "bullet"}
    
    return text_input, uploaded_file, length_map[length_option], format_map[format_option]