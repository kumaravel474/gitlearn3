import requests
from bs4 import BeautifulSoup
import time

# Telegram Configuration
TELEGRAM_BOT_TOKEN = "7875275535:AAFoNQXjkW1D6Wrl8liaYjlFCmCgbxij8gU"
TELEGRAM_CHAT_ID = "-1002282196044"

# Amazon Deals URL (Electronics)
AMAZON_URL = "https://www.amazon.in/deals?ref_=nav_cs_gb&discounts-widget=%2522%257B%255C%2522state%255C%2522%253A%257B%255C%2522refinementFilters%255C%2522%253A%257B%255C%2522percentOff%255C%2522%253A%255B%255C%25223%255C%2522%255D%257D%257D%252C%255C%2522version%255C%2522%253A1%257D%2522"

# Headers (to bypass Amazon bot detection)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5",
}

def get_loot_deals():
    """Scrape Amazon for loot deals"""
    response = requests.get(AMAZON_URL, headers=HEADERS)
    if response.status_code != 200:
        print("❌ Failed to fetch Amazon deals")
        return []

    soup = BeautifulSoup(response.text, "lxml")
    deals = []

    for item in soup.select(".DealCard-module__dealCard_1-xYf"):
        title = item.select_one(".DealContent-module__truncate_3PzR7").text.strip()
        link = "https://www.amazon.in" + item.select_one("a")["href"]
        discount_text = item.select_one(".BadgeAutomated-module__badge_1d-VR").text.strip()
        
        if "%" in discount_text:
            discount = int(discount_text.replace("%", "").replace("off", "").strip())
            if discount >= 40:
                deals.append((title, link, discount))

    return deals

def send_to_telegram(deals):
    """Send deals to Telegram"""
    if not deals:
        message = "⚠️ No loot deals found!"
    else:
        message = "🔥 *Amazon Loot Deals (40%+ Off)* 🔥\n\n"
        for title, link, discount in deals:
            message += f"🔹 *{title}* - {discount}% Off\n🔗 [Buy Now]({link})\n\n"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, data=data)

if __name__ == "__main__":
    while True:
        print("🔍 Scraping Amazon Deals Page...")
        loot_deals = get_loot_deals()
        send_to_telegram(loot_deals)
        print("✅ Deals sent to Telegram! Waiting 20 minutes...\n")
        time.sleep(1200)  # Wait 20 minutes (1200 seconds)