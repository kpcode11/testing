import pdfplumber

def extract_text_pdfplumber(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

pdf_text = extract_text_pdfplumber("C:/Users/praja/OneDrive/Desktop/Python Projects/pdf_processing/44_ExpNo.1_Keshav.pdf")
print(pdf_text)

