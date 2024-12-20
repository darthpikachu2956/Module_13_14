from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = "xxx"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

keyboard_bas = ReplyKeyboardMarkup(resize_keyboard=True)
button3 = KeyboardButton(text="Count")
button4 = KeyboardButton(text='Information')
keyboard_bas.add(button3)
keyboard_bas.add(button4)

keyboard = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text="Calculate norma of calories", callback_data="calories")
button2 = InlineKeyboardButton(text="Calculating formula", callback_data="formulas")
keyboard.add(button1)
keyboard.add(button2)


@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer("Hello! I am a healthcare bot!", reply_markup=keyboard_bas)


@dp.message_handler(lambda message: message.text == "Count")
async def main_menu(message):
    await message.answer("Select an option:", reply_markup=keyboard)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("The formula is: 10 * weight + 6,25 * growth – 5 * age + 5")
    await call.answer()


@dp.message_handler(text="Information")
async def inform(message):
    await message.answer("Information about this bot.")


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Input your age, please.")
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


@dp.message_handler()
async def all_message(message):
    await message.answer("Please input the '/start' command in order to begin the communication.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
