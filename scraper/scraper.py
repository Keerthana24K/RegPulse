import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_pdf(pdf_url, filename):
    """Downloads a single PDF file given its full URL."""
    output_dir = os.path.join("data", "pdfs")
    os.makedirs(output_dir, exist_ok=True)
    
    local_filepath = os.path.join(output_dir, filename)
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        print(f"-> Downloading file: {filename}...")
        response = requests.get(pdf_url, headers=headers, stream=True, timeout=30)
        
        if response.status_code == 200:
            with open(local_filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"✅ Successfully saved to: {local_filepath}")
        else:
            print(f"❌ Failed to download PDF. Status: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Error saving PDF {filename}: {e}")

def run_scraper():
    """Main function to parse the notification list and locate PDFs."""
    base_url = "https://www.rbi.org.in/Scripts/NotificationUser.aspx"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print("Fetching recent RBI notification indices...")
    try:
        response = requests.get(base_url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print("❌ We are being blocked by the website's firewall!")
            return
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 🌟 FIX: Instead of hunting for a specific CSS class name, 
        # let's look for any link ('a' tag) that points to a Notification item.
        links = []
        for anchor in soup.find_all("a"):
            href = anchor.get("href", "")
            # RBI circular links always contain 'Id=' followed by numbers
            if "notificationuser.aspx?id=" in href.lower():
                links.append(anchor)
        
        print(f"Found {len(links)} notification links on the main table.")
        
        if len(links) == 0:
            print("⚠️ Could not match any notification links. Let's inspect the page layout.")
            return

        # Process the top 2 latest items
        for index, link in enumerate(links[:2]):
            href = link.get("href")
            full_page_url = urljoin("https://www.rbi.org.in/Scripts/", href)
            print(f"\n[{index+1}] Inspecting Circular Page: {full_page_url}")
            
            page_res = requests.get(full_page_url, headers=headers, timeout=15)
            page_soup = BeautifulSoup(page_res.text, "html.parser")
            
            pdf_link_found = False
            for anchor in page_soup.find_all("a"):
                anchor_href = anchor.get("href", "")
                if ".pdf" in anchor_href.lower():
                    full_pdf_url = urljoin(full_page_url, anchor_href)
                    
                    filename = anchor_href.split("/")[-1]
                    if not filename.endswith(".pdf"):
                        filename = f"circular_{index+1}.pdf"
                        
                    download_pdf(full_pdf_url, filename)
                    pdf_link_found = True
                    break 
            
            if not pdf_link_found:
                print("ℹ️ No raw PDF attachment found on this notice landing page.")
                
    except Exception as e:
        print(f"Scraper encountered structural error: {e}")

if __name__ == "__main__":
    run_scraper()