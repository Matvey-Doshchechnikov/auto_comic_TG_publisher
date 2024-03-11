import requests
import telegram
import os
import random
from dotenv import load_dotenv


def download_random_xkcd_comic(comic_url):
    response = requests.get(comic_url)
    response.raise_for_status()
    last_comic_number = response.json()['num']
    random_comic_number = random.randint(1, last_comic_number)
    test_url = f"https://xkcd.com//{random_comic_number}/info.0.json"
    response = requests.get(test_url)
    response.raise_for_status()
    comic_png_url = response.json()['img']
    image_response = requests.get(comic_png_url)
    image_response.raise_for_status()
    filename = 'test.png'
    with open(filename, 'wb') as file:
        file.write(image_response.content)


def send_picture(image, chat_id, bot):
    with open(image, 'rb') as file:
        bot.send_document(
            chat_id=chat_id,
            document=file
        )


if __name__ == "__main__":
    comic_url = "https://xkcd.com/info.0.json"
    download_random_xkcd_comic(comic_url)
    load_dotenv()
    tg_token = os.environ['TELEGRAM_TOKEN']
    bot = telegram.Bot(token=tg_token)
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    try:
        send_picture('test.png', chat_id, bot)
    finally:
        if os.path.exists('test.png'):
            os.remove('test.png')
