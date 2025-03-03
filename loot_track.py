import requests
from bs4 import BeautifulSoup
from telegram import Bot

# Telegram bot details
TELEGRAM_BOT_TOKEN = "7875275535:AAFoNQXjkW1D6Wrl8liaYjlFCmCgbxij8gU"
TELEGRAM_CHAT_ID = "-1002282196044"

# URL to scrape
URL = "https://pricehistory.app/"

# Discount threshold (e.g., 50%)
DISCOUNT_THRESHOLD = 50

def fetch_deals():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve data: {response.status_code}")
        return None

def parse_deals(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    deals = []

    # Locate the section containing the deals
    deals_section = soup.find_all("div", class_="flex flex-col bg-white rounded-lg shadow-md overflow-hidden")
    if not deals_section:
        print("No deals section found.")
        return deals

    for deal in deals_section:
        try:
            # Extract deal details
            title = deal.find("h2", class_="text-lg font-semibold text-gray-900").text.strip()
            original_price = deal.find("span", class_="line-through text-gray-500").text.strip()
            discounted_price = deal.find("span", class_="text-lg font-semibold text-gray-900").text.strip()
            discount_percentage = deal.find("span", class_="text-red-600").text.strip()
            image_url = deal.find("img", class_="w-full")["src"]
            deal_link = deal.find("a", class_="block mt-2")["href"]

            # Convert prices to float for calculation
            original_price_value = float(original_price.replace("₹", "").replace(",", ""))
            discounted_price_value = float(discounted_price.replace("₹", "").replace(",", ""))

            # Calculate the actual discount percentage
            calculated_discount = ((original_price_value - discounted_price_value) / original_price_value) * 100

            # Filter deals based on the discount threshold
            if calculated_discount >= DISCOUNT_THRESHOLD:
                deals.append({
                    "title": title,
                    "original_price": original_price,
                    "discounted_price": discounted_price,
                    "discount_percentage": f"{calculated_discount:.2f}%",
                    "image_url": image_url,
                    "deal_link": deal_link
                })
        except Exception as e:
            print(f"Error parsing deal: {e}")
            continue

    return deals

def send_to_telegram(deals):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    for deal in deals:
        message = (
            f"🔥 *{deal['title']}*\n"
            f"💰 *Original Price:* {deal['original_price']}\n"
            f"💸 *Discounted Price:* {deal['discounted_price']}\n"
            f"🔖 *Discount:* {deal['discount_percentage']}\n"
            f"[🔗 View Deal]({deal['deal_link']})"
        )
        bot.send_photo(
            chat_id=TELEGRAM_CHAT_ID,
            photo=deal['image_url'],
            caption=message,
            parse_mode="Markdown"
        )

if __name__ == "__main__":
    html_content = fetch_deals()
    if html_content:
        deals = parse_deals(html_content)
        if deals:
            send_to_telegram(deals)
        else:
            print("No deals found with the specified discount threshold.")
    else:
        print("Failed to retrieve the webpage content.")