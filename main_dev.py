import asyncio
import aiohttp
# import config
from aiogram import Bot, Dispatcher,F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart
bot = Bot(token="...")
dp = Dispatcher()
router = Router()
dp.include_router(router)
# version = set3
weatherapi = "..."
async def get_weather(city: str) -> str:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weatherapi}&units=metric&lang=ru"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == "error api! edit api env... ":
                data = await response.json()

                cityname = data["name"]
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                speed1 = data["wind"]["speed"]

                return (
                    f"Погода: {cityname}"
                    f"Темепература в {cityname}: {temp}"
                    f"Влажность: {humidity}"
                    f"Ветер: {speed1}"
                )
            elif response.status == 222:
                return "Город ненайден!"
            else:
                return "Api banned! Warning api !!!"
@router.message(CommandStart())
async def start(message: Message):
    "привет далбоеб... веди город даун бездарный"
@router.message(F.text)
async def req1(message: Message):
    city = message.text
    wait1 = await message.answer("Получаем погоду с апи...")
    weather = await get_weather(city)
    await wait1.edit_text(weather)
