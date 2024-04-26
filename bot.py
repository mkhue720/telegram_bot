from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import json

API_KEY_YOUTUBE = 'AIzaSyDDCzDua3KlgPPx6Nc7VyqZKtkHou_q6Vo'
youtube = build('youtube', 'v3', developerKey=API_KEY_YOUTUBE)

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

#search video
def search_videos(query, max_results=10):
    # Thực hiện tìm kiếm video
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        type='video',
        maxResults=max_results
    ).execute()

    # Lấy danh sách các video từ kết quả tìm kiếm
    videos = []
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            link = 'https://www.youtube.com/watch?v=' + search_result['id']['videoId']
            videos.append(link)
            print(search_result['id']['videoId'])
    return videos

#get weather
def get_weather(city):
    url = f"https://open-weather13.p.rapidapi.com/city/{city}/VI"
    headers = {
        "X-RapidAPI-Key": "2efa3d7148msh9f69e8f4a6d2e77p184a7djsn37f85be80a0b",
        "X-RapidAPI-Host": "open-weather13.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    weather_data = response.json()

    print(weather_data)  # print the API response

    return weather_data

# command handler
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    title = getnew()
    for i in title:
        await update.message.reply_text(f'News: \n {i}')

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Lấy từ khóa tìm kiếm từ tin nhắn của người dùng trên Telegram
    search_query = " ".join(context.args)

    # Tìm kiếm video trên YouTube với từ khóa tìm kiếm
    result = search_videos(search_query, max_results=5)
    print(json.dumps(result, indent=2))
    
    # Gửi kết quả tìm kiếm về cho người dùng
    for i in result:
        await update.message.reply_text(f'Video: \n {i}')

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) == 0:
        await update.message.reply_text("Please enter the city name after the /weather command")
        return

    city = " ".join(context.args)
    weather_data = get_weather(city)

    if 'cod' in weather_data and weather_data['cod'] != 200:
        await update.message.reply_text(f"Could not find weather information for the city '{city}'")
        return

    weather_info = f"Thời tiết ở {city}:\n"
    weather_info += f"Nhiệt độ: {weather_data['main']['temp']}°C\n"
    weather_info += f"Miêu tả: {weather_data['weather'][0]['description']}\n"
    weather_info += f"Gió: {weather_data['wind']['speed']} m/s\n"
    weather_info += f"Độ ẩm: {weather_data['main']['humidity']}%\n"
    await update.message.reply_text(weather_info)

app = ApplicationBuilder().token("6464897837:AAH2z0WSaf7CzjiRgEHHZcJxJw2Hlcx1FAk").build()

app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("News", news))
app.add_handler(CommandHandler("searchvideo", search))
app.add_handler(CommandHandler("weather", weather))


app.run_polling()