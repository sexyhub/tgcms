from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
import requests

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your CMS bot.')

def echo(update: Update, context: CallbackContext) -> None:
    keyword = update.message.text

    cms_link = fetch_cms_link(keyword)

    if cms_link:
        update.message.reply_text(cms_link)
    else:
        update.message.reply_text(f"No link found for keyword: {keyword}")

def fetch_cms_link(keyword):
    api_url = "https://nxshare.top/m/api.php"
    response = requests.get(api_url)
    data = response.json()

    for item in data:
        if keyword in item['title']:
            return item['url']

    return None

def main():
    # Replace "YOUR_BOT_TOKEN" with your actual bot token
    bot_token = "1633187381:AAEx4Ap-RV7RfFzSfqhY1JePEEIJ9v9IRYc"
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
