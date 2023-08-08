from pyrogram import Client, filters

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = '1633187381:AAEx4Ap-RV7RfFzSfqhY1JePEEIJ9v9IRYc'

app = Client("my_bot", bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start(client, message):
    message.reply_text("Hello! I am your CMS bot.")

@app.on_message(~filters.command)
def echo(client, message):
    keyword = message.text

    cms_link = fetch_cms_link(keyword)

    if cms_link:
        message.reply_text(cms_link)
    else:
        message.reply_text(f"No link found for keyword: {keyword}")

def fetch_cms_link(keyword):
    api_url = "https://nxshare.top/m/api.php"
    response = requests.get(api_url)
    data = response.json()

    for item in data:
        if keyword in item['title']:
            return item['url']

    return None

if __name__ == '__main__':
    app.run()
