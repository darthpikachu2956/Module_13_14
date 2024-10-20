from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = "XXXXX"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(text=["Urban", "ff"])
async def urban_message(message):
    print("Urban message.")


@dp.message_handler(commands=["start"])
async def start(message):
    print("Hello! I am a healthcare bot!")


@dp.message_handler()
async def all_message(message):
    print("Please input a '/start' command in order to begin the communication.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
