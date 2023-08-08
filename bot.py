import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Telegram Bot token
BOT_TOKEN = '1633187381:AAEx4Ap-RV7RfFzSfqhY1JePEEIJ9v9IRYc'

# Your CMS API endpoint for fetching post links based on title
CMS_API_URL = 'https://nxshare.top/m/api.php'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! I am your CMS Bot. Send me a post title to get the link.')

def handle_message(update: Update, context: CallbackContext) -> None:
    post_title = update.message.text.strip()

    # Fetch post links from the CMS API
    response = requests.get(CMS_API_URL)
    if response.status_code == 200:
        posts = response.json()
        matching_posts = [post for post in posts if post['title'].lower() == post_title.lower()]
        if matching_posts:
            post_link = matching_posts[0]['url']
            update.message.reply_text(f"Here's the link to the post '{post_title}': {post_link}")
        else:
            update.message.reply_text(f"No post found with the title '{post_title}'.")
    else:
        update.message.reply_text("Error fetching data from CMS.")

def main() -> None:
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
