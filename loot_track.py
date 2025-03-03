import requests
from bs4 import BeautifulSoup
import telegram

# Set your Telegram bot details
TELEGRAM_BOT_TOKEN = "7875275535:AAFoNQXjkW1D6Wrl8liaYjlFCmCgbxij8gU"
TELEGRAM_CHAT_ID = "-1002282196044"

# Amazon Loot Deals URL (Change based on your location)
AMAZON_URL = "https://www.amazon.in/deals"

# Function to scrape Amazon deals
def get_amazon_loot_deals():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(AMAZON_URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    deals = []
    for deal in soup.select(".DealCard-module__card_3c4d6"):
        try:
            title = deal.select_one(".DealContent-module__truncate_sWbxET").text.strip()
            price = deal.select_one(".a-price .a-offscreen").text.strip()
            discount = deal.select_one(".BadgeAutomatedLabel-module__badgeText_1b25c").text.strip()
            image = deal.select_one(".a-image-container img")["src"]
            link = "https://www.amazon.in" + deal.select_one("a")["href"]

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
        message = f"🔥 *{title}*\n💰 *Price:* {price}\n🔖 *Discount:* {discount}\n[🔗 View on Amazon]({link})"
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=image, caption=message, parse_mode="Markdown")

# Main Execution
deals = get_amazon_loot_deals()
if deals:
    send_to_telegram(deals)
else:
    print("No loot deals found!")