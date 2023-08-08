import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Your Telegram Bot token
BOT_TOKEN = '1633187381:AAEx4Ap-RV7RfFzSfqhY1JePEEIJ9v9IRYc'

# Function to handle /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! I am your CMS Bot. Send me a post title to get the link.')

# Function to handle text messages
def handle_message(update: Update, context: CallbackContext) -> None:
    post_title = update.message.text.strip()  # Extract the post title from the message
    # Replace spaces with underscores to match your CMS URL structure
    post_title_normalized = post_title.replace(' ', '_')
    post_link = f'https://your-cms-website.com/posts/{post_title_normalized}'
    update.message.reply_text(f"Here's the link to the post '{post_title}': {post_link}")

def main() -> None:
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    
    # Add message handler for text messages
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
