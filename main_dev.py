# Импорт фреймворка
# Dev ==  @ownerkernelsunext
import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher,F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
router = Router()
weatherapi = "..."
token1 = "..."
#получение погоды через апи опен веатхер и aiohttp
async def get_weather(city: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weatherapi}&units=metric&lang=ru"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                temp = data["main"]["temp"]
                description = data["weather"][0]["description"].capitalize()
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]
                return (
                    f"Погода в {city}:\n"

                    f"  Температура в городе: {temp}°С\n"
                    f"  Описание погоды: {description}\n"
                    f"  Влажность: {humidity}%\n"
                    f"  Ветер: {wind_speed} м/с"
                )
            
            elif response.status == 401:
                return "Ключ невалидный бро..."
            return f"Город не найден {response.status}"
            
@router.message(CommandStart())
async def start(message: Message):
    "привет dtlb ujhjl"

@router.message(F.text)
async def req1(message: Message):
    city = message.text
    wait1 = await message.answer("Получаем погоду с апи...")
    weather = await get_weather(city)
    await wait1.edit_text(weather)


async def main():
    bot = Bot(token=token1)
    dp = Dispatcher()
    dp.include_router(router)
    print("ыыыы")
    await dp.start_polling(bot)
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("styartss no")