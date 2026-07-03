import os
import pdfplumber

def extract_text_from_pdf(pdf_path):
    """Opens a single PDF file and extracts all visible text content."""
    extracted_text = ""
    
    try:
        # Open the PDF file using pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Reading: {os.path.basename(pdf_path)} ({len(pdf.pages)} pages found)")
            
            # Loop through every single page in the document
            for index, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                
                if page_text:
                    extracted_text += f"\n--- PAGE {index + 1} ---\n"
                    extracted_text += page_text
                    
        return extracted_text
        
    except Exception as e:
        print(f"❌ Error reading PDF at {pdf_path}: {e}")
        return None

def process_downloaded_pdfs():
    """Scans the data/pdfs directory and extracts text from available files."""
    pdf_dir = os.path.join("data", "pdfs")
    
    # Safety Check: Verify the folder exists
    if not os.path.exists(pdf_dir):
        print(f"❌ Target folder '{pdf_dir}' not found. Run your scraper first!")
        return

    # Find all files ending with .pdf inside our data folder
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]
    
    if not pdf_files:
        print("⚠️ No PDF files found to parse inside data/pdfs/.")
        return

    print(f"Found {len(pdf_files)} files available for text conversion.\n")
    
    # Process just the first PDF for our testing run today
    target_file = pdf_files[0]
    full_path = os.path.join(pdf_dir, target_file)
    
    print(f"==============================")
    text_content = extract_text_from_pdf(full_path)
    print(f"==============================")
    
    if text_content:
        # Print out the first 500 characters of the extracted text so we can verify it works
        print("\n--- Snippet of Extracted Content ---")
        print(text_content[:500] + "\n...")
        print("------------------------------------")
        print("✅ Text successfully isolated and readable!")

if __name__ == "__main__":
    process_downloaded_pdfs()