import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from telegram import Bot

# ✅ Setup Telegram bot
TELEGRAM_BOT_TOKEN = "7875275535:AAFoNQXjkW1D6Wrl8liaYjlFCmCgbxij8gU"
TELEGRAM_CHAT_ID = "-1002282196044"

# ✅ Amazon Loot Deals URL (Modify if needed)
AMAZON_URL = "https://www.amazon.in/deals?filter=percent-off-50-"

# ✅ Setup Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without opening a browser
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def fetch_amazon_deals():
    """Scrape Amazon deals page for loot offers above 50% off."""
    driver.get(AMAZON_URL)
    time.sleep(5)  # Wait for page to load

    soup = BeautifulSoup(driver.page_source, "html.parser")
    deals = []

    for item in soup.find_all("div", class_="DealCard-module__dealCard_3opzP"):
        try:
            title = item.find("span", class_="a-size-medium").text.strip()
            price = item.find("span", class_="a-price-whole").text.strip()
            discount = item.find("span", class_="a-size-base-plus").text.strip()
            image_url = item.find("img")["src"]
            link = "https://www.amazon.in" + item.find("a", class_="a-link-normal")["href"]

            if "off" in discount and int(discount.replace("% off", "").strip()) >= 50:
                deals.append({
                    "title": title,
                    "price": f"₹{price}",
                    "discount": discount,
                    "image_url": image_url,
                    "link": link
                })
        except Exception as e:
            print(f"Error parsing deal: {e}")
            continue

    return deals

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
    deals = fetch_amazon_deals()
    if deals:
        send_to_telegram(deals)
    else:
        print("No loot deals found!")
    
    driver.quit()  # Close the browser