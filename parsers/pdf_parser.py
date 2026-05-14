import fitz

def extractTextFromPDF(pdf_path):
    text = ""

    try:
        pdf_doc = fitz.open(pdf_path)

        for page in pdf_doc:
            text += page.get_text()

        pdf_doc.close()

        return text
    except Exception as e:
        return f"Error reading PDF: {e}"
    