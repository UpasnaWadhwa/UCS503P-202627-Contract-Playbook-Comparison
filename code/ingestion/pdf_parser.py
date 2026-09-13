import pdfplumber

def extract_text(file_path: str) -> str:
    """Extract raw text from a PDF or plain text file."""
    if file_path.lower().endswith(".pdf"):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
