import requests
from bs4 import BeautifulSoup
import time
import random

# Configuration
AMAZON_BASE = "https://www.amazon.in"
ELECTRONICS_URL = f"{AMAZON_BASE}/s?k=electronics&i=electronics&ref=nb_sb_noss_2"
CHECK_INTERVAL = 600  # 10 minutes

# Enhanced headers to mimic a real browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.amazon.in/",
    "DNT": "1"
}

def get_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching page: {str(e)}")
        return None

def parse_electronics_items(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = []
    
    # Look for product containers using updated selectors
    for item in soup.select('div.s-main-slot div[data-component-type="s-search-result"]'):
        try:
            # Extract product title
            title_elm = item.select_one('h2 a span')
            if not title_elm:
                continue
            title = title_elm.get_text(strip=True)
            
            # Extract product URL
            url_elm = item.select_one('h2 a')
            if not url_elm:
                continue
            url = AMAZON_BASE + url_elm['href']
            
            # Extract price
            price_elm = item.select_one('.a-price .a-offscreen')
            if not price_elm:
                continue
            price = price_elm.get_text(strip=True)
            
            # Extract rating
            rating_elm = item.select_one('.a-icon-star-small .a-icon-alt')
            rating = rating_elm.get_text(strip=True) if rating_elm else "No rating"
            
            # Extract number of reviews
            reviews_elm = item.select_one('.a-size-base.s-underline-text')
            reviews = reviews_elm.get_text(strip=True) if reviews_elm else "No reviews"
            
            items.append({
                'title': title,
                'url': url,
                'price': price,
                'rating': rating,
                'reviews': reviews
            })
            
            # Stop after 15 items
            if len(items) >= 15:
                break
        except Exception as e:
            print(f"Error parsing item: {str(e)}")
            continue
            
    return items

def print_items(items):
    print("\n📱 **Current Electronics Items on Amazon** 📱")
    for i, item in enumerate(items, 1):
        print(f"\n{i}. {item['title']}")
        print(f"   💰 Price: {item['price']}")
        print(f"   ⭐ Rating: {item['rating']}")
        print(f"   📝 Reviews: {item['reviews']}")
        print(f"   🔗 Link: {item['url']}")
    print("\n" + "=" * 50 + "\n")

def main():
    while True:
        print(f"🕒 Fetching electronics items... (Next update in {CHECK_INTERVAL // 60} minutes)")
        html = get_page(ELECTRONICS_URL)
        if html:
            items = parse_electronics_items(html)
            if items:
                print_items(items)
            else:
                print("No items found. Check if Amazon has blocked the request or the HTML structure has changed.")
        else:
            print("Failed to fetch items. Check your internet connection.")
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    print("🚀 Starting Electronics Item Tracker...")
    main()