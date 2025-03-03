from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from telegram import Bot
import time

# Telegram Configuration
TELEGRAM_BOT_TOKEN = "7875275535:AAFoNQXjkW1D6Wrl8liaYjlFCmCgbxij8gU"
TELEGRAM_CHAT_ID = "-1002282196044"


# Amazon Deals URL
AMAZON_DEALS_URL = "https://www.amazon.in/deals?ref_=nav_cs_gb&discounts="

def scrape_amazon_deals():
    """Scrape Amazon for loot deals (above 50% discount)"""
    try:
        # Firefox options
        options = Options()
        options.add_argument("--headless")  # Run Firefox in headless mode

        # Start WebDriver with Geckodriver
        driver = webdriver.Firefox(service=Service("/data/data/com.termux/files/usr/bin/geckodriver"), options=options)
        driver.get(AMAZON_DEALS_URL)
        time.sleep(5)

        deals = []
        deal_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'DealCard-module__card')]")

        for deal in deal_elements:
            try:
                title = deal.find_element(By.XPATH, ".//span[contains(@class, 'DealContent-module__truncate')]").text.strip()
                discount_text = deal.find_element(By.XPATH, ".//span[contains(@class, 'BadgeAutomatedLabel-module__badge')]").text.strip()

                if "%" in discount_text:
                    discount = int(discount_text.replace("%", "").strip())
                    if discount >= 20:
                        price = deal.find_element(By.XPATH, ".//span[contains(@class, 'PriceString-module__price')]").text.strip()
                        image_url = deal.find_element(By.XPATH, ".//img[contains(@class, 'Image-module__image')]").get_attribute("src")
                        link = deal.find_element(By.XPATH, ".//a[contains(@class, 'DealLink-module__link')]").get_attribute("href")

                        deals.append({
                            "title": title,
                            "price": price,
                            "discount": f"{discount}% off",
                            "image_url": image_url,
                            "link": link
                        })
            except Exception as e:
                print(f"Error parsing deal: {e}")
                continue

        driver.quit()
        return deals

    except Exception as e:
        print(f"Amazon Scraping Failed: {e}")
        return []

def send_to_telegram(deals):
    """Send deals to Telegram"""
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
    deals = scrape_amazon_deals()

    if deals:
        send_to_telegram(deals)
        print("✅ Deals sent to Telegram!")
    else:
        print("⚠️ No loot deals found!")