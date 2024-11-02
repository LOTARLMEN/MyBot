from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from my_api import ONLY_MY_API
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton("Рассчёт калорий")
kb.add(button)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


api = ONLY_MY_API
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет', reply_markup=kb)

@dp.message_handler(text="Рассчёт калорий")
async def set_age(message):
    await message.answer("Введите ваш возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите ваш рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите ваш вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    # Для мужчин
    bmr_male = 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) - 5 + 5
    # Для женщин
    bmr_female = 10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) - 161
    await message.answer(f'Для мужчин норма калорий для таких характеристик: {bmr_male}\n'
                         f'Для женщин норма калорий для таких характеристик: {bmr_female}')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
