import requests
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Bot

# ✅ Configure Telegram bot
TELEGRAM_BOT_TOKEN = "7875275535:AAFoNQXjkW1D6Wrl8liaYjlFCmCgbxij8gU"
TELEGRAM_CHAT_ID = "-1002282196044"

# ✅ Amazon Deals Page
AMAZON_DEALS_URL = "https://www.amazon.in/deals?ref_=nav_cs_gb"

# ✅ Fake headers to bypass detection
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def scrape_amazon_deals():
    """Scrape Amazon for loot deals (above 50% discount)"""
    try:
        print("🔍 Scraping Amazon Deals Page...")
        response = requests.get(AMAZON_DEALS_URL, headers=HEADERS)
        
        if response.status_code != 200:
            print("⚠️ Failed to fetch Amazon page")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        deals = []

        for item in soup.find_all("div", class_="DealContent-module__truncate_sWbxETx42ZPStTc9jwySW"):
            try:
                title = item.text.strip()
                discount_element = item.find_next("span", class_="a-size-base a-color-secondary")
                
                if discount_element:
                    discount_text = discount_element.text.strip()
                    if "%" in discount_text:
                        discount = int(discount_text.replace("% off", "").strip())

                        if discount >= 50:
                            price_element = item.find_next("span", class_="a-price-whole")
                            price = price_element.text.strip() if price_element else "Unknown Price"

                            image_element = item.find_previous("img")
                            image_url = image_element["src"] if image_element else None

                            link_element = item.find_previous("a", href=True)
                            link = f"https://www.amazon.in{link_element['href']}" if link_element else "#"

                            deals.append({
                                "title": title,
                                "price": f"₹{price}",
                                "discount": f"{discount}% off",
                                "image_url": image_url,
                                "link": link
                            })
            except Exception as e:
                print(f"⚠️ Error parsing deal: {e}")
                continue

        return deals

    except Exception as e:
        print(f"❌ Amazon Scraping Failed: {e}")
        return []

def send_to_telegram(deals):
    """Send deals to Telegram channel."""
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    for deal in deals:
        message = (
            f"🔥 *{deal['title']}*\n"
            f"💰 *Price:* {deal['price']}\n"
            f"🔖 *Discount:* {deal['discount']}\n"
            f"[🔗 View Deal]({deal['link']})"
        )
        bot.send_photo(
            chat_id=TELEGRAM_CHAT_ID,
            photo=deal['image_url'],
            caption=message,
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    deals = scrape_amazon_deals()

    if deals:
        send_to_telegram(deals)
        print("✅ Deals sent to Telegram!")
    else:
        print("⚠️ No loot deals found!")