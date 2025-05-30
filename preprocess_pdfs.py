#preprocess pdfs and save to make the text ready for training
#We create combined_text.txt from local PDFs
from pdf_data import load_local_pdfs, extract_and_clean, combine_texts

def preprocess_and_save():
    pdf_folder = "local_pdfs"
    pdf_files = load_local_pdfs(pdf_folder)
    all_texts = [extract_and_clean(pdf) for pdf in pdf_files]
    combined = combine_texts(all_texts)
    
    with open("combined_text.txt", "w", encoding="utf-8") as f:
        f.write(combined)
    print("Preprocessing done! combined_text.txt created.")

if __name__ == "__main__":
    preprocess_and_save()
