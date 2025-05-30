import os
import re
import fitz  # PyMuPDF for PDF handling


#Function to clean extracted text from PDFs

def clean_text(text):
    
    text = text.replace('\n', ' ').replace('\xa0', ' ')# replace newlines and non-breaking spaces
    text = re.sub(r'\s{2,}', ' ', text)  # remove extra spaces
    text = re.sub(r'[^\x20-\x7EÅÄÖåäö\s]', '', text)  # keep characters that are printable in UTF-8, including Swedish characters
    return text.strip() #.strip() removes leading and trailing whitespace


#Load local PDF files from local folder
def load_local_pdfs(folder_path):

    pdf_paths = []
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(".pdf"):
            full_path = os.path.join(folder_path, file_name)
            pdf_paths.append(full_path)
    return pdf_paths

def extract_and_clean(pdf_path): 
    # Extracts text from a PDF file and cleans it.
    with fitz.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf:
            full_text += page.get_text()
    return clean_text(full_text)

# Combines multiple texts into a single string with double newlines between them
def combine_texts(texts):
    return "\n\n".join(texts).strip()
