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
    keyword = message.text.lower()  # Convert the message text to lowercase for case-insensitive matching

    cms_links = fetch_cms_links(keyword)

    if cms_links:
        links_message = "\n".join(cms_links)
        bot.reply_to(message, f"Links for keyword '{keyword}':\n{links_message}")
    else:
        bot.reply_to(message, f"No links found for keyword '{keyword}'")

def fetch_cms_links(keyword):
    api_url = "https://nxshare.top/m/api.php"
    response = requests.get(api_url)
    data = response.json()

    matching_links = []

    for item in data:
        if keyword in item['title'].lower():  # Convert title to lowercase for case-insensitive matching
            matching_links.append(item['url'])

    return matching_links

bot.polling()
