from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

api = "xxx"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text="Calories")
async def set_age(message):
    await message.answer("Input your age, please.")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Input your growth, please.")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Input your weight, please.")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data.get('age'))
    growth = float(data.get('growth'))
    weight = float(data.get('weight'))
    result = (10 * weight) + (6.25 * growth) - (5 * age) + 5
    await message.answer(f"Your normal calories consuming is {result}.")
    await state.finish()


@dp.message_handler(commands=["start"])
async def start(message):
    print("A message is received.")
    await message.answer("Hello! I am a healthcare bot!")


@dp.message_handler()
async def all_message(message):
    print("A message is received.")
    await message.answer("Please input the '/start' command in order to begin the communication.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
