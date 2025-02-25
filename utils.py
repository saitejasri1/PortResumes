import PyPDF2

def extract_text_from_resume(uploaded_file):
    """
    Extracts text from a PDF resume using PyPDF2.
    """
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text
