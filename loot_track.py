import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from telegram import Bot

# ✅ Configure Telegram bot
TELEGRAM_BOT_TOKEN = "your_bot_token_here"
TELEGRAM_CHAT_ID = "your_chat_id_here"

# ✅ Amazon Loot Deals URL (Modify if needed)
AMAZON_URL = "https://www.amazon.in/deals?filter=percent-off-50-"

# ✅ Setup Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run without opening a browser
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def fetch_amazon_deals():
    """Scrape Amazon deals page for loot offers above 50% off."""
    driver.get(AMAZON_URL)
    time.sleep(5)  # Wait for page to load

    # ✅ Scroll down to load more deals
    body = driver.find_element(By.TAG_NAME, "body")
    for _ in range(5):  # Scroll multiple times
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

    deals = []
    deal_elements = driver.find_elements(By.CSS_SELECTOR, "div.a-section.a-spacing-none.gbhq-deal-card")

    for item in deal_elements:
        try:
            title = item.find_element(By.CSS_SELECTOR, "span.a-text-normal").text.strip()
            price = item.find_element(By.CSS_SELECTOR, "span.a-price-whole").text.strip()
            discount = item.find_element(By.CSS_SELECTOR, "span.a-size-mini.s-coupon-highlight-color").text.strip()
            image_url = item.find_element(By.TAG_NAME, "img").get_attribute("src")
            link = item.find_element(By.TAG_NAME, "a").get_attribute("href")

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