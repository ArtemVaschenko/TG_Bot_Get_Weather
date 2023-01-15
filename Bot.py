import requests
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher

from config import Token, open_wether_token

bot = Bot(token=Token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("hello input the name of your city to get weather info:")


@dp.message_handler()
async def get_getweather(message: types.Message):
    try:
        r = requests.get(
            f'http://api.openweathermap.org/geo/1.0/direct?q={message.text}&appid={open_wether_token}'
        )
        d = r.json()

        lat = d[0]["lat"]
        lon = d[0]['lon']
        name = d[0]['name']

        re = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={open_wether_token}&units=metric'
        )
        data = re.json()

        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']

        await message.reply(
            f'The weather in {name} is {weather} \n'
            f'real tempreture is {int(round(temp, 0))}°C \n'
            f'fells like {int(round(feels_like, 0))}°C')

    except:
        await message.reply('Check name of the city')


if __name__ == '__main__':
    executor.start_polling(dp)
