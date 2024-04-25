from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup

def getnew():
    title = []
    r = requests.get('https://baomoi.com/tag/LITE.epi')

    soup = BeautifulSoup(r.text, 'html.parser')

    mydivs = soup.find_all("h3", {"class": "font-semibold block"})

    for new in mydivs:
        link = 'https://baomoi.com' + new.a.get('href')
        title.append(link)
        print(new.a.get('href'))
    return title

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    title = getnew()
    for i in title:
        await update.message.reply_text(f'News: \n {i}')


app = ApplicationBuilder().token("6464897837:AAH2z0WSaf7CzjiRgEHHZcJxJw2Hlcx1FAk").build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("News", news))

app.run_polling()