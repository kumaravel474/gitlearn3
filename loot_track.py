import requests

# Telegram Configuration
TELEGRAM_BOT_TOKEN = "7875275535:AAFoNQXjkW1D6Wrl8liaYjlFCmCgbxij8gU"
TELEGRAM_CHAT_ID = "-1002282196044"

# Amazon Sample Link
amazon_link = "https://amzn.in/d/5E9EyJL"
message = f"🔥 *Amazon Loot Deal:* [Click Here]({amazon_link})"

# Telegram API URL
url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}

# Send the message
response = requests.post(url, data=data)

# Check Response
if response.status_code == 200:
    print("✅ Link sent to Telegram!")
else:
    print("❌ Failed to send. Error:", response.text)