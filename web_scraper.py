import requests
from bs4 import BeautifulSoup
import csv
import json
import time

# Define the URL and headers for the request
BASE_URL = "https://quotes.toscrape.com/page/{}/"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# Function to scrape data
def scrape_quotes(max_pages=5):
    all_quotes = []  # List to store all quotes

    for page in range(1, max_pages + 1):
        try:
            # Send the GET request
            response = requests.get(BASE_URL.format(page), headers=HEADERS)
            response.raise_for_status()  # Raise exception for HTTP errors

            # Parse the HTML content
            soup = BeautifulSoup(response.text, "html.parser")

            # Find all quote elements
            quotes = soup.find_all("div", class_="quote")
            if not quotes:
                print(f"No quotes found on page {page}. Reached the last page.")
                break

            # Extract quote details
            for quote in quotes:
                text_tag = quote.find("span", class_="text")
                author_tag = quote.find("small", class_="author")
                tag_elements = quote.find_all("a", class_="tag")

                # Safely extract text, author, and tags
                text = text_tag.get_text(strip=True) if text_tag else "No text"
                author = author_tag.get_text(strip=True) if author_tag else "Unknown author"
                tags = [tag.get_text(strip=True) for tag in tag_elements]

                # Append to the list
                all_quotes.append({"text": text, "author": author, "tags": tags})

            # Check for pagination
            if not soup.find("li", class_="next"):
                print("No next page found. Scraping complete.")
                break

            # Sleep to avoid overloading the server
            time.sleep(1)

        except Exception as e:
            print(f"Error on page {page}: {e}")

    return all_quotes

# Function to save data to CSV
def save_to_csv(data, filename="scraped_quotes.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["text", "author", "tags"])
        writer.writeheader()
        for row in data:
            # Join tags into a single string for CSV
            row["tags"] = ", ".join(row["tags"])
            writer.writerow(row)
    print(f"Data saved to {filename}")

# Function to save data to JSON
def save_to_json(data, filename="scraped_quotes.json"):
    with open(filename, mode="w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")

# Main function
if __name__ == "__main__":
    print("Starting to scrape quotes...")
    quotes_data = scrape_quotes(max_pages=10)

    if quotes_data:
        save_to_csv(quotes_data)
        save_to_json(quotes_data)
    else:
        print("No quotes were scraped.")
