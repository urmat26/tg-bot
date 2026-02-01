import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, command
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from aiogram.types import Message
import httpx
load_dotenv()

TOKEN= os.getenv('TOKEN')
API_KEY = os.getenv('API_KEY')

bot = Bot(token=TOKEN)
dp = Dispatcher()


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "deepseek/deepseek-chat"

async def ask_ai(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "altynbekoffBot",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Ты полезный помощник. Отвечай понятно, без воды."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.3,
    }

    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(OPENROUTER_URL, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()

    return data["choices"][0]["message"]["content"]

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Напиши вопрос — я отвечу 🤖")

@dp.message(F.text)
async def handle_text(message: Message):
    try:
        answer = await ask_ai(message.text)
        if len(answer) > 3900:
            answer = answer[:3900] + "...\n\n(ответ обрезан)"
        await message.answer(answer)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())