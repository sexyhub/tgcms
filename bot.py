import telebot
import requests

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = '1633187381:AAEx4Ap-RV7RfFzSfqhY1JePEEIJ9v9IRYc'

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! I am your CMS bot.")

@bot.message_handler(func=lambda message: True)
def echo(message):
    keyword = message.text

    cms_link = fetch_cms_link(keyword)

    if cms_link:
        bot.send_message(message.chat.id, cms_link)
    else:
        bot.send_message(message.chat.id, f"No link found for keyword: {keyword}")

def fetch_cms_link(keyword):
    api_url = "https://nxshare.top/m/api.php"
    response = requests.get(api_url)
    data = response.json()

    for item in data:
        if keyword in item['title']:
            return item['url']

    return None

bot.polling()
