from docx import Document

def extractTextFromDocx(docx_path):
    text = ""

    try:
        doc = Document(docx_path)

        for para in doc.paragraphs:
            text += para.text + "\n"

        return text
    
    except Exception as e:
        return f"Error reading DOCX: {e}"
    