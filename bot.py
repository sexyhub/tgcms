import requests
import time
import threading
import telebot
from telebot import types

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = 'YOUR_BOT_TOKEN'

bot = telebot.TeleBot(BOT_TOKEN)

RESULTS_PER_PAGE = 5
cms_links = []

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! I am your CMS bot.")

@bot.message_handler(func=lambda message: True)
def search_links(message):
    global cms_links

    start_time = time.time()

    keyword = message.text.lower()
    cms_links = fetch_cms_links(keyword)

    if cms_links:
        send_links_with_pagination(message.chat.id, message.message_id, message.from_user.username, keyword, start_time)
    else:
        bot.send_message(message.chat.id, f"No links found for keyword '{keyword}'")

def fetch_cms_links(keyword):
    api_url = "https://nxshare.top/m/api.php"
    response = requests.get(api_url)
    data = response.json()

    matching_links = []

    for item in data:
        if keyword in item['title'].lower():
            matching_links.append({'title': item['title'], 'url': item['url']})

    return matching_links

def send_links_with_pagination(chat_id, reply_to_message_id, requested_by, query, start_time):
    global cms_links

    start_idx = 0
    end_idx = min(RESULTS_PER_PAGE, len(cms_links))
    links_to_send = cms_links[start_idx:end_idx]

    markup = generate_keyboard_buttons(links_to_send)

    end_time = time.time()
    time_taken = end_time - start_time

    reply_msg = f"""
Tʜᴇ Rᴇꜱᴜʟᴛꜱ Fᴏʀ ☞ {query}
Rᴇǫᴜᴇsᴛᴇᴅ Bʏ ☞ @{requested_by}
ʀᴇsᴜʟᴛ sʜᴏᴡ ɪɴ ☞ {time_taken:.2f} seconds
ᴘᴏᴡᴇʀᴇᴅ ʙʏ ☞ Okflix
⚠️ ᴀꜰᴛᴇʀ 5 ᴍɪɴᴜᴛᴇꜱ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇᴅ 🗑️
"""

    image_url = "https://images.hdqwalls.com/wallpapers/bthumb/black-panther-wakanda-forever-4k-artwork-zu.jpg"

    bot.send_photo(chat_id, image_url, caption=reply_msg, reply_markup=markup, parse_mode='HTML', reply_to_message_id=reply_to_message_id)

    # Schedule the deletion of the message after 5 minutes
    time_to_delete = time.time() + 300  # 300 seconds = 5 minutes
    schedule_deletion(chat_id, reply_to_message_id, time_to_delete)

def generate_keyboard_buttons(links):
    markup = types.InlineKeyboardMarkup(row_width=1)

    for link in links:
        button = types.InlineKeyboardButton(text=link['title'], url=link['url'])
        markup.add(button)

    return markup

def schedule_deletion(chat_id, message_id, delete_at):
    def delete_message():
        bot.delete_message(chat_id, message_id)

    time_to_wait = delete_at - time.time()
    if time_to_wait > 0:
        deletion_timer = threading.Timer(time_to_wait, delete_message)
        deletion_timer.start()

bot.polling()
