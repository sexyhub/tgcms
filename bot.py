import requests
import time
import threading
import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode
from aiogram.utils import executor

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = '6220396148:AAGAPu-M2S-PQP5XjypJM9gvz5E3dLQsQvc'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

RESULTS_PER_PAGE = 5
cms_links = []

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Hello! I am your CMS bot.")

@dp.message_handler(lambda message: True)
async def echo(message: types.Message):
    global cms_links
    
    start_time = time.time()  # Record the start time
    
    keyword = message.text.lower()  # Convert the message text to lowercase for case-insensitive matching

    cms_links = fetch_cms_links(keyword)

    if cms_links:
        await send_links_with_pagination(message, keyword, start_time)
    else:
        await message.reply(f"No links found for keyword '{keyword}'")

def fetch_cms_links(keyword):
    api_url = "https://nxshare.top/m/api.php"
    response = requests.get(api_url)
    data = response.json()

    matching_links = []

    for item in data:
        if keyword in item['title'].lower():  # Convert title to lowercase for case-insensitive matching
            matching_links.append({'title': item['title'], 'url': item['url']})

    return matching_links

async def send_links_with_pagination(message: types.Message, query, start_time):
    start_idx = 0
    end_idx = min(RESULTS_PER_PAGE, len(cms_links))
    links_to_send = cms_links[start_idx:end_idx]

    markup = generate_keyboard_buttons(links_to_send)
    
    end_time = time.time()  # Record the end time
    time_taken = end_time - start_time
    
    reply_msg = f"""
Tʜᴇ Rᴇꜱᴜʟᴛꜱ Fᴏʀ ☞ {query}
    
Rᴇǫᴜᴇsᴛᴇᴅ Bʏ ☞ @{message.from_user.username}
    
ʀᴇsᴜʟᴛ sʜᴏᴡ ɪɴ ☞ {time_taken:.2f} seconds
    
ᴘᴏᴡᴇʀᴇᴅ ʙʏ ☞ : Okflix
    
⚠️ ᴀꜰᴛᴇʀ 5 ᴍɪɴᴜᴛᴇꜱ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴅᴇʟᴇᴛᴇᴅ 🗑️
"""

    image_url = "https://images.hdqwalls.com/wallpapers/bthumb/black-panther-wakanda-forever-4k-artwork-zu.jpg"

    await bot.send_photo(message.chat.id, photo=image_url, caption=reply_msg, reply_markup=markup, parse_mode=ParseMode.HTML)

    # Schedule the deletion of the replied message after 5 minutes
    time_to_delete = time.time() + 300  # 300 seconds = 5 minutes
    schedule_deletion(message.chat.id, message.message_id, time_to_delete)

def generate_keyboard_buttons(links):
    markup = types.InlineKeyboardMarkup(row_width=1)

    for link in links:
        button = types.InlineKeyboardButton(text=link['title'], url=link['url'])
        markup.insert(button)

    return markup

def schedule_deletion(chat_id, message_id, delete_at):
    async def delete_message():
        await bot.delete_message(chat_id, message_id)
    
    time_to_wait = delete_at - time.time()
    if time_to_wait > 0:
        loop = asyncio.get_event_loop()
        loop.call_later(time_to_wait, asyncio.ensure_future, delete_message())

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
