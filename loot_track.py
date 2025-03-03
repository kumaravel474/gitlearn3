import requests
import telegram
from bs4 import BeautifulSoup

# Telegram bot details
TELEGRAM_BOT_TOKEN = "7875275535:AAFoNQXjkW1D6Wrl8liaYjlFCmCgbxij8gU"
TELEGRAM_CHAT_ID = "-1002282196044"

# PriceHistory Amazon Loot Deals URL
URL = "https://pricehistory.app/amazon-deal-finder"

# Function to scrape deals
def get_loot_deals():
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    deals = []
    for deal in soup.select(".grid.grid-cols-1.md\\:grid-cols-3.lg\\:grid-cols-4.gap-4 a"):
        try:
            title = deal.select_one(".text-sm.font-medium.text-gray-900").text.strip()
            price = deal.select_one(".text-lg.font-semibold.text-gray-900").text.strip()
            discount = deal.select_one(".text-red-600").text.strip()
            image = deal.select_one("img")["src"]
            link = "https://pricehistory.app" + deal["href"]

            # Extract discount percentage
            discount_percentage = int(discount.replace("% off", "").strip())
            if discount_percentage >= 50:  # Only 50%+ off deals
                deals.append((title, price, discount, image, link))
        except:
            continue

    return deals

# Function to send deals to Telegram
def send_to_telegram(deals):
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    for title, price, discount, image, link in deals:
        message = f"🔥 *{title}*\n💰 *Price:* {price}\n🔖 *Discount:* {discount}\n[🔗 View Deal]({link})"
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=image, caption=message, parse_mode="Markdown")

# Main Execution
deals = get_loot_deals()
print(response.text)  # Print full page source

if deals:
    send_to_telegram(deals)
else:
    print("No loot deals found!")