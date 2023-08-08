import telebot
import requests
from telebot import types

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = 'YOUR_BOT_TOKEN'

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! I am your CMS bot.")

@bot.message_handler(func=lambda message: True)
def echo(message):
    keyword = message.text.lower()  # Convert the message text to lowercase for case-insensitive matching

    cms_links = fetch_cms_links(keyword)

    if cms_links:
        markup = generate_keyboard_buttons(cms_links)
        bot.send_message(message.chat.id, f"Links for keyword '{keyword}':", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f"No links found for keyword '{keyword}'")

def fetch_cms_links(keyword):
    api_url = "https://nxshare.top/m/api.php"
    response = requests.get(api_url)
    data = response.json()

    matching_links = []

    for item in data:
        if keyword in item['title'].lower():  # Convert title to lowercase for case-insensitive matching
            matching_links.append({'title': item['title'], 'url': item['url']})

    return matching_links

def generate_keyboard_buttons(links):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    for link in links:
        button = types.KeyboardButton(f"🔗 {link['title']}")
        markup.add(button)

    return markup

bot.polling()
