import fitz  # PyMuPDF
import sys
import os

def extract_text(pdf_path, txt_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Successfully extracted {pdf_path} to {txt_path}")
    except Exception as e:
        print(f"Error extracting {pdf_path}: {e}")

if __name__ == "__main__":
    base_dir = "/Users/istiakahmmedbishal/Desktop/Thesis"
    pdfs = [
        ("papers/researchpaper32.pdf", "knowledge_base/paper_extracts/paper_32_extract.txt"),
        ("papers/researchpaper33.pdf", "knowledge_base/paper_extracts/paper_33_extract.txt"),
        ("papers/researchpaper34.pdf", "knowledge_base/paper_extracts/paper_34_extract.txt"),
    ]
    
    for pdf_rel, txt_rel in pdfs:
        pdf_path = os.path.join(base_dir, pdf_rel)
        txt_path = os.path.join(base_dir, txt_rel)
        extract_text(pdf_path, txt_path)
