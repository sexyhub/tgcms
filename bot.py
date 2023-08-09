import telebot

# Replace 'YOUR_API_TOKEN' with the actual API token provided by BotFather
API_TOKEN = '1633187381:AAEx4Ap-RV7RfFzSfqhY1JePEEIJ9v9IRYc'

# Create a new instance of the TeleBot class
bot = telebot.TeleBot(API_TOKEN)

# Handle the '/start' command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! I'm your bot. Type /help for assistance.")

# Handle the '/help' command
@bot.message_handler(commands=['help'])
def help(message):
    response = "This is a simple bot. Here are the available commands:\n"
    response += "/start - Start interacting with the bot\n"
    response += "/help - Display this help message"
    bot.reply_to(message, response)

# Handle all other messages
@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, f"You said: {message.text}")

# Polling loop to keep the bot running
bot.polling()
