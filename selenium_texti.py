import sys
import time
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def sanitize_title(title):
    return re.sub(r'\W+', '_', title.strip())

def scrape_with_selenium(url, output_file=None):
    try:
        # Setup headless Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        time.sleep(5)  # Tunggu JS load

        # Ambil judul
        page_title = driver.title
        clean_title = sanitize_title(page_title)

        if not output_file:
            output_file = f"selenium_title_{clean_title}.txt"

        # Ambil semua teks dari body
        content = driver.find_element(By.TAG_NAME, 'body').text

        # Simpan ke file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[✓] Success: Saved to {output_file}")

        driver.quit()
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        try: driver.quit()
        except: pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python selenium_scraper.py <url> [output.txt]")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    scrape_with_selenium(url, output_file)
