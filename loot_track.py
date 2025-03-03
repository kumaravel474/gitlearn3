import requests
import json
from telegram import Bot

# ✅ Configure Telegram bot (Replace with your credentials)
# ✅ Configure Telegram bot
TELEGRAM_BOT_TOKEN = "7875275535:AAFoNQXjkW1D6Wrl8liaYjlFCmCgbxij8gU"
TELEGRAM_CHAT_ID = "-1002282196044"

# ✅ Amazon API URL (Unofficial)
AMAZON_URL = "https://www.amazon.in/deals/ajax?filter=percent-off-50-"

# ✅ PriceHistory API URL
PRICEHISTORY_URL = "https://pricehistory.app/amazon-deal-finder"

# ✅ Fake headers to avoid blocking
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def fetch_amazon_deals():
    """Fetch deals from Amazon JSON API (Unofficial)"""
    try:
        response = requests.get(AMAZON_URL, headers=HEADERS)
        if response.status_code != 200:
            print("Failed to load Amazon page")
            return []

        data = json.loads(response.text)
        deals = []

        for item in data.get("deals", []):
            title = item["title"]
            price = item["price"]["current_price"]
            discount = item["discount_percent"]
            image_url = item["image"]
            link = f"https://www.amazon.in/dp/{item['asin']}"

            if discount >= 50:
                deals.append({
                    "title": title,
                    "price": f"₹{price}",
                    "discount": f"{discount}% off",
                    "image_url": image_url,
                    "link": link
                })

        return deals

    except Exception as e:
        print(f"Amazon API failed: {e}")
        return []

def fetch_pricehistory_deals():
    """Fetch deals from PriceHistory API (Alternative Source)"""
    try:
        response = requests.get(PRICEHISTORY_URL, headers=HEADERS)
        if response.status_code != 200:
            print("Failed to load PriceHistory page")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        deals = []

        for item in soup.find_all("div", class_="deal-card"):
            try:
                title = item.find("h2").text.strip()
                price = item.find("span", class_="deal-price").text.strip()
                discount = item.find("span", class_="deal-discount").text.strip()
                image_url = item.find("img")["src"]
                link = item.find("a")["href"]

                if "off" in discount and int(discount.replace("% off", "").strip()) >= 50:
                    deals.append({
                        "title": title,
                        "price": price,
                        "discount": discount,
                        "image_url": image_url,
                        "link": link
                    })
            except Exception as e:
                print(f"Error parsing deal: {e}")
                continue

        return deals

    except Exception as e:
        print(f"PriceHistory API failed: {e}")
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
    # Try Amazon API first
    deals = fetch_amazon_deals()

    # If no deals found, try PriceHistory API
    if not deals:
        print("Amazon API failed, trying PriceHistory API...")
        deals = fetch_pricehistory_deals()

    if deals:
        send_to_telegram(deals)
    else:
        print("No loot deals found!")