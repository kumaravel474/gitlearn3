import requests
from bs4 import BeautifulSoup
import time
import json
import asyncio
from telegram import Bot
from telegram.error import TelegramError
import re

# Configuration
TELEGRAM_BOT_TOKEN = "7875275535:AAFoNQXjkW1D6Wrl8liaYjlFCmCgbxij8gU"
TELEGRAM_CHAT_ID = "-1002282196044"
CHECK_INTERVAL = 900  # 15 minutes
PRODUCTS_FILE = "electronics_deals.json"
MIN_DISCOUNT = 50
MAX_DISCOUNT = 80

AMAZON_DEALS_URL = "https://www.amazon.in/gp/deals?ref_=nav_cs_gb&category=electronics"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36",
    "Accept-Language": "en-IN, en;q=0.9"
}

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def load_products():
    try:
        with open(PRODUCTS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_products(products):
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f, indent=2)

async def get_deal_page():
    try:
        response = requests.get(AMAZON_DEALS_URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching deals page: {str(e)}")
        return None

def parse_deals(html):
    soup = BeautifulSoup(html, 'html.parser')
    deals = []
    
    for item in soup.select('div.dealTile'):
        try:
            # Extract discount percentage
            discount_text = item.select_one('.a-text-price').get_text()
            discount = int(re.search(r'\d+', discount_text).group())
            
            if MIN_DISCOUNT <= discount <= MAX_DISCOUNT:
                title = item.select_one('.a-size-base.a-link-normal').get_text(strip=True)
                url = "https://amazon.in" + item.select_one('a.a-link-normal')['href']
                price = float(item.select_one('span.a-price-whole').get_text().replace(',', ''))
                
                # Get original price
                original_price_elm = item.select_one('.a-text-price[data-a-strike]')
                original_price = float(original_price_elm.get_text().replace('₹', '').replace(',', '')) if original_price_elm else None
                
                deals.append({
                    'title': title,
                    'url': url,
                    'current_price': price,
                    'original_price': original_price,
                    'discount': discount,
                    'last_checked': time.time()
                })
        except Exception as e:
            print(f"Error parsing deal: {str(e)}")
            continue
            
    return deals

async def check_deals():
    html = await get_deal_page()
    if not html:
        return
    
    current_deals = parse_deals(html)
    tracked_deals = load_products()
    
    for deal in current_deals:
        product_id = deal['url'].split('/dp/')[-1].split('/')[0]
        
        if product_id not in tracked_deals:
            # New deal found
            message = f"🔥 New Electronics Deal! 🔥\n"
            message += f"📱 {deal['title']}\n"
            message += f"💰 Price: ₹{deal['current_price']:,.2f}\n"
            if deal['original_price']:
                message += f"📉 {deal['discount']}% OFF (Was ₹{deal['original_price']:,.2f})\n"
            message += f"🔗 Link: {deal['url']}"
            
            try:
                await bot.send_message(
                    chat_id=TELEGRAM_CHAT_ID,
                    text=message
                )
                tracked_deals[product_id] = deal
            except TelegramError as e:
                print(f"Telegram error: {str(e)}")
        else:
            # Check price drop
            old_price = tracked_deals[product_id]['current_price']
            if deal['current_price'] < old_price:
                message = f"🚨 Price Drop Alert! 🚨\n"
                message += f"📱 {deal['title']}\n"
                message += f"⬇️ From ₹{old_price:,.2f} to ₹{deal['current_price']:,.2f}\n"
                message += f"🔗 Link: {deal['url']}"
                
                try:
                    await bot.send_message(
                        chat_id=TELEGRAM_CHAT_ID,
                        text=message
                    )
                    tracked_deals[product_id] = deal
                except TelegramError as e:
                    print(f"Telegram error: {str(e)}")
    
    save_products(tracked_deals)

async def main():
    while True:
        start_time = time.time()
        await check_deals()
        elapsed = time.time() - start_time
        await asyncio.sleep(max(CHECK_INTERVAL - elapsed, 0))

if __name__ == "__main__":
    print("🚀 Starting Electronics Deal Tracker...")
    asyncio.run(main())