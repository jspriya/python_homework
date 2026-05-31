import json
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Task 3: Write a Program to Extract this Data

def main():
    # 1. Setup options and initialize the Chrome WebDriver browser session
    options = webdriver.ChromeOptions()
    print("Initializing Chrome browser using native Selenium Manager...")
    driver = webdriver.Chrome(options=options)
    
    # 2. Define the assignment URL 
    target_url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"
    print(f"Loading web page: {target_url}")
    driver.get(target_url)
    
    # 3. Use Explicit Waits to safely wait for the dynamic content to render
    print("Waiting for dynamic catalog elements to load on screen...")
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.cp-search-result-item"))
        )
        time.sleep(3) # buffer for background text components to populate fully
    except Exception as e:
        print(f"Error: Timeout waiting for page elements to load. {e}")
        driver.quit()
        return

    # 4. Find book result elements using reliable multi-class selector strategies
    print("Locating search result items...")
    book_elements = driver.find_elements(By.CSS_SELECTOR, "li.cp-search-result-item")
    print(f"Incremental Check: Found {len(book_elements)} book entries on the page.")
    
    # 5. Initialize the results storage list structure
    results = []
    
    # 6. Main iteration loop through the catalog search result card rows
    for index, book in enumerate(book_elements, start=1):
        try:
            # --- EXTRACT TITLE ---
            try:
                title_el = book.find_element(By.CSS_SELECTOR, ".cp-title")
                title_text = title_el.text.strip().split('\n')[0]
            except Exception:
                title_text = "Unknown Title"

            # --- EXTRACT AUTHORS ---
            author_elements = book.find_elements(By.CSS_SELECTOR, "a.author-link")
            author_list = [author.text.strip() for author in author_elements if author.text.strip()]
            author_text = "; ".join(author_list) if author_list else "Unknown Author"
            
            # --- EXTRACT FORMAT-YEAR ---
            format_year_text = "Unknown Format"
            try:
                # Break down the absolute entire text output block of the single book card container
                all_card_lines = [line.strip() for line in book.text.split('\n') if line.strip()]
                
                # Scan the list of text rows to isolate rows containing key library formats
                found_formats = []
                for line in all_card_lines:
                    if any(kwd in line for kwd in ["Book", "eBook", "Audiobook", "Streaming Video", "Video"]):
                        if "shel" not in line.lower() and "check out" not in line.lower():
                            found_formats.append(line)
                if found_formats:
                    format_year_text = " / ".join(list(set(found_formats)))
                else:
                    details_container = book.find_element(By.CSS_SELECTOR, "div.manifestation-details, [class*='format']")
                    format_year_text = details_container.text.strip().replace('\n', ' ')
            except Exception:
                format_year_text = "Format/Year unavailable"
            
            # 7. Create dictionary mapping for the single item entry record row
            book_dict = {
                "Title": title_text,
                "Author": author_text,
                "Format-Year": format_year_text
            }
            results.append(book_dict)
            
        except Exception as e:
            continue

    # 8. Close and quit the background browser process cleanly
    print("Scraping completed. Terminating browser session...")
    driver.quit()
    
    # 9. Data structuring: Build a modern DataFrame out of the list of dicts
    print("\nAssembling Pandas DataFrame object structure:")
    df = pd.DataFrame(results)

    
    # 10. Output results: Print and export data structures to files
    print("======================================================================")
    if not df.empty:
        with pd.option_context('display.max_colwidth', 50):
            print(df.to_string(index=False))
            
    # --- TASK 4: Write the DataFrame out to get_books.csv ---
        csv_filename = "get_books.csv"
        df.to_csv(csv_filename, index=False, encoding='utf-8')
        print(f"\n[Task 4] SUCCESS: CSV dataset exported directly to file: {csv_filename}")
        
        # --- TASK 4: Write the results list out to get_books.json ---
        json_filename = "get_books.json"
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(results, json_file, indent=4, ensure_ascii=False)
        print(f"[Task 4] SUCCESS: JSON data exported directly to file: {json_filename}")
    else:
        print("DataFrame is empty. Please verify the page structure elements.")
    print("======================================================================")

if __name__ == "__main__":
    main()