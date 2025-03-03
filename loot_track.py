from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from telegram import Bot
import time

# Telegram Configuration
TELEGRAM_BOT_TOKEN = "7875275535:AAFoNQXjkW1D6Wrl8liaYjlFCmCgbxij8gU"
TELEGRAM_CHAT_ID = "-1002282196044"

# Amazon Deals Page
AMAZON_DEALS_URL = "https://www.amazon.in/deals?ref_=nav_cs_gb"

def scrape_amazon_links():
    """Scrape Amazon Deals Page and extract product links"""
    try:
        # Setup Firefox options
        options = Options()
        options.add_argument("--headless")  # Run Firefox in headless mode

        # Start WebDriver with Geckodriver
        driver = webdriver.Firefox(service=Service("/data/data/com.termux/files/usr/bin/geckodriver"), options=options)
        driver.get(AMAZON_DEALS_URL)
        time.sleep(5)

        product_links = []
        deal_elements = driver.find_elements(By.XPATH, "//a[contains(@class, 'DealLink-module__link')]")

        for deal in deal_elements:
            link = deal.get_attribute("href")
            if link and "amazon" in link:
                product_links.append(link)

        driver.quit()
        return product_links

    except Exception as e:
        print(f"Amazon Scraping Failed: {e}")
        return []

def send_to_telegram(links):
    """Send product links to Telegram"""
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    message = "🔥 *Amazon Loot Deals:*\n\n" + "\n".join(links)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="Markdown")

if __name__ == "__main__":
    links = scrape_amazon_links()

    if links:
        send_to_telegram(links)
        print("✅ Product links sent to Telegram!")
    else:
        print("⚠️ No product links found!")