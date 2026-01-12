from PyPDF2 import PdfReader

def extract_text_from_pdf(uploaded_file):
    """Mengekstrak teks dari file PDF."""
    try:
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text
    except Exception as e:
        return None