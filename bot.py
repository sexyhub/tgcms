import telebot
import requests
from telebot import types

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = '1633187381:AAEx4Ap-RV7RfFzSfqhY1JePEEIJ9v9IRYc'

bot = telebot.TeleBot(BOT_TOKEN)

RESULTS_PER_PAGE = 5
current_page = 0
cms_links = []

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! I am your CMS bot.")

@bot.message_handler(func=lambda message: True)
def echo(message):
    global cms_links, current_page
    
    keyword = message.text.lower()  # Convert the message text to lowercase for case-insensitive matching

    cms_links = fetch_cms_links(keyword)
    current_page = 0

    if cms_links:
        send_links_with_pagination(message.chat.id, message.message_id)
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
    markup = types.InlineKeyboardMarkup(row_width=1)

    for link in links:
        button = types.InlineKeyboardButton(text=link['title'], url=link['url'])
        markup.add(button)

    return markup

def send_links_with_pagination(chat_id, reply_to_message_id):
    global cms_links, current_page

    start_idx = current_page * RESULTS_PER_PAGE
    end_idx = start_idx + RESULTS_PER_PAGE
    links_to_send = cms_links[start_idx:end_idx]

    markup = generate_keyboard_buttons(links_to_send)
    reply_msg = f"Links (Page {current_page + 1}):"

    image_url = "https://images.hdqwalls.com/wallpapers/bthumb/black-panther-wakanda-forever-4k-artwork-zu.jpg"

    # Send the image as a separate photo message
    bot.send_photo(chat_id, photo=image_url, reply_to_message_id=reply_to_message_id)

    # Send the reply message with buttons
    bot.send_message(chat_id, reply_msg, reply_markup=markup, parse_mode='HTML')

bot.polling()
