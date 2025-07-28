from pdfminer.high_level import extract_text

def extract_text_from_pdf(file_path):
    try:
        return extract_text(file_path)
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        return ""
