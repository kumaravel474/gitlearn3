from telegram import Bot

# Telegram Configuration
# Telegram Configuration
TELEGRAM_BOT_TOKEN = "7875275535:AAFoNQXjkW1D6Wrl8liaYjlFCmCgbxij8gU"
TELEGRAM_CHAT_ID = "-1002282196044"

# Amazon Sample Link
amazon_link = "https://amzn.in/d/5E9EyJL"

def send_sample_link():
    """Send a sample Amazon deal link to Telegram"""
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    message = f"🔥 *Amazon Loot Deal:* [Click Here]({amazon_link})"
    
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="Markdown")

if __name__ == "__main__":
    send_sample_link()
    print("✅ Sample link sent to Telegram!")