import requests
from bs4 import BeautifulSoup
import time
import json
import asyncio
from telegram import Bot
from telegram.error import TelegramError
import re
from datetime import datetime

# Configuration
TELEGRAM_BOT_TOKEN = "7875275535:AAFoNQXjkW1D6Wrl8liaYjlFCmCgbxij8gU"
TELEGRAM_CHAT_ID = "-1002282196044"
CHECK_INTERVAL = 60  # Check every 10 minutes
PRODUCTS_FILE = "time_based_deals.json"
MIN_DISCOUNT = 50
MAX_DISCOUNT = 80

# Amazon URLs
AMAZON_BASE = "https://www.amazon.in"
LIGHTNING_DEALS_URL = f"{AMAZON_BASE}/gp/deals?ref_=nav_cs_gb"

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

async def get_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching page: {str(e)}")
        return None

def parse_lightning_deals(html):
    soup = BeautifulSoup(html, 'html.parser')
    deals = []
    
    # Look for Lightning Deal containers
    for item in soup.select('[data-component-type="s-deals-grid-item"]'):
        try:
            # Extract deal time
            time_remaining = item.select_one('.a-text-bold .a-color-base')
            if not time_remaining:
                continue
                
            # Extract discount percentage
            discount_elm = item.select_one('.a-text-price')
            if not discount_elm:
                continue
                
            discount_text = discount_elm.get_text()
            discount_match = re.search(r'\d+', discount_text)
            if not discount_match:
                continue
                
            discount = int(discount_match.group())
            
            if MIN_DISCOUNT <= discount <= MAX_DISCOUNT:
                title_elm = item.select_one('h2 a')
                if not title_elm:
                    continue
                    
                title = title_elm.get_text(strip=True)
                url = AMAZON_BASE + title_elm['href']
                
                price_elm = item.select_one('.a-price .a-offscreen')
                if not price_elm:
                    continue
                    
                price = float(price_elm.get_text().replace('₹', '').replace(',', ''))
                
                # Get original price
                original_price_elm = item.select_one('.a-text-price[data-a-strike]')
                original_price = float(original_price_elm.get_text().replace('₹', '').replace(',', '')) if original_price_elm else None
                
                deals.append({
                    'title': title,
                    'url': url,
                    'current_price': price,
                    'original_price': original_price,
                    'discount': discount,
                    'time_remaining': time_remaining.get_text(strip=True),
                    'last_checked': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        except Exception as e:
            print(f"Error parsing deal: {str(e)}")
            continue
            
    return deals

async def check_lightning_deals():
    html = await get_page(LIGHTNING_DEALS_URL)
    if not html:
        return
    
    current_deals = parse_lightning_deals(html)
    tracked_deals = load_products()
    
    for deal in current_deals:
        product_id = deal['url'].split('/dp/')[-1].split('/')[0]
        
        if product_id not in tracked_deals:
            # New deal found
            message = f"⏳ **Time-Based Deal Alert!** ⏳\n"
            message += f"🕒 Time Remaining: {deal['time_remaining']}\n"
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
        await check_lightning_deals()
        elapsed = time.time() - start_time
        await asyncio.sleep(max(CHECK_INTER requests
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
CHECK_INTERVAL = 1800  # 30 minutes
PRODUCTS_FILE = "electronics_deals.json"
MIN_DISCOUNT = 50
MAX_DISCOUNT = 80

# Updated Amazon URLs
AMAZON_BASE = "https://www.amazon.in"
AMAZON_DEALS_URL = f"{AMAZON_BASE}/gp/deals"
ELECTRONICS_URL = f"{AMAZON_BASE}/s?k=electronics&i=electronics&bbn=976419031&ref=nb_sb_noss"

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

async def get_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)  # Reduced timeout
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching page: {str(e)}")
        return None

def parse_deals(html):
    soup = BeautifulSoup(html, 'html.parser')
    deals = []
    
    # Look for deal containers
    for item in soup.select('[data-component-type="s-search-result"]'):
        try:
            # Extract discount percentage
            discount_elm = item.select_one('.a-text-price')
            if not discount_elm:
                continue
                
            discount_text = discount_elm.get_text()
            discount_match = re.search(r'\d+', discount_text)
            if not discount_match:
                continue
                
            discount = int(discount_match.group())
            
            if MIN_DISCOUNT <= discount <= MAX_DISCOUNT:
                title_elm = item.select_one('h2 a')
                if not title_elm:
                    continue
                    
                title = title_elm.get_text(strip=True)
                url = AMAZON_BASE + title_elm['href']
                
                price_elm = item.select_one('.a-price .a-offscreen')
                if not price_elm:
                    continue
                    
                price = float(price_elm.get_text().replace('₹', '').replace(',', ''))
                
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
    # Try multiple URLs
    urls_to_try = [
        ELECTRONICS_URL,
        AMAZON_DEALS_URL
    ]
    
    for url in urls_to_try:
        html = await get_page(url)
        if html:
            break
    else:
        print("Failed to fetch deals from all URLs")
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