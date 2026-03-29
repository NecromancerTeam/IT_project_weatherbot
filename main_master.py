# Импорт фреймворка
# Dev ==  @ownerkernelsunext
import os
import asyncio
import aiohttp
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher,F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.utils.keyboard import InlineKeyboardBuilder
load_dotenv()
router = Router()
weatherapi = os.getenv("weatherapiconf")
token1 = os.getenv("tokenconf")
async def weather1(city: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weatherapi}&units=metric&lang=ru"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data1 = await response.json()
                temp  = data1["main"]["temp"]
                description = data1["weather"][0]["description"].capitalize()
                hum = data1["main"]["humidity"]
                windspeed = data1["wind"]["speed"]
                return (
                    f"Погода в {city}:\n"
                    f"  Температура в городе: {temp}°С\n"
                    f"  Описание погоды: {description}\n"
                    f"  Влажность: {hum}%\n"
                    f"  Ветер: {windspeed} м/с"
                )            
            elif response.status == 401:
                return "Ключ невалидный бро..."
            return f"Город не найден {response.status}"
@router.message(CommandStart())
async def start(message: Message):
    await message.answer("пр,веди город свой")

@router.message(F.text)
async def req1(message: Message):
    city = message.text
    wait1 = await message.answer("Получаем погоду с апи...")
    weather = await weather1(city)
    await wait1.edit_text(weather)
#инлпйн, можно вырезать
@router.inline_query()
async def inline_handler(query: InlineQuery):
    city = query.query.strip()
    if not city:
        return
    weather_data = await weather1(city)
    results = [
        InlineQueryResultArticle(
            id=f"weather_{city}",
            title="Получить погоду",
            description=f"получить погоду в {city}",
            input_message_content=InputTextMessageContent(
                message_text=weather_data
            )
        )
    ]
    await query.answer(results=results, cache_time=1)
async def main():
    bot = Bot(token=token1)
    dp = Dispatcher()
    dp.include_router(router)
    print("бот запущен и работает")
    await dp.start_polling(bot)
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот отключен")