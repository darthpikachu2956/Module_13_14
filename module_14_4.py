from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *

api = "xxx"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

keyboard_bas = ReplyKeyboardMarkup(resize_keyboard=True)
button3 = KeyboardButton(text="Count")
button4 = KeyboardButton(text="Information")
keyboard_bas.add(button3, button4)
button5 = KeyboardButton(text="Buy")
keyboard_bas.add(button5)

keyboard = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text="Calculate norma of calories", callback_data="calories")
button2 = InlineKeyboardButton(text="Calculating formula", callback_data="formulas")
keyboard.add(button1)
keyboard.add(button2)

keyboard_buy = InlineKeyboardMarkup()
buy_but1 = InlineKeyboardButton(text="Product 1", callback_data="product_buying")
buy_but2 = InlineKeyboardButton(text="Product 2", callback_data="product_buying")
buy_but3 = InlineKeyboardButton(text="Product 3", callback_data="product_buying")
buy_but4 = InlineKeyboardButton(text="Product 4", callback_data="product_buying")
keyboard_buy.row(buy_but1, buy_but2, buy_but3, buy_but4)


@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer("Hello! I am a healthcare bot!", reply_markup=keyboard_bas)
    get_all_products()


@dp.message_handler(text="Information")
async def inform(message):
    await message.answer("Information about this bot.")


@dp.message_handler(lambda message: message.text == "Count")
async def main_menu(message):
    await message.answer("Select an option:", reply_markup=keyboard)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("The formula is: 10 * weight + 6,25 * growth – 5 * age + 5")
    await call.answer()


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


@dp.message_handler(text="Buy")
async def get_buying_list(message):
    products = get_all_products()
    for product in products:
        product_id = product[0]
        title = product[1]
        description = product[2]
        price = product[3]
        await message.answer(f"Name: {title} | Description: {description} | Price: {price} USD.")
        with open(f'files/pills{product_id}.png', "rb") as img:
            await message.answer_photo(img)
    await message.answer("Select a product to purchase:", reply_markup=keyboard_buy)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("You have successfully purchased the item!")


@dp.message_handler()
async def all_message(message):
    await message.answer("Please input the '/start' command in order to begin the communication.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
