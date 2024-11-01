import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import dotenv

dotenv.load_dotenv()
ONLY_MY_API = os.getenv("ONLY_MY_API")

kb = ReplyKeyboardMarkup([[KeyboardButton("Рассчитать калории"),
                           KeyboardButton("Информация")]]
                         , resize_keyboard=True)
# button = KeyboardButton("Рассчитать калории")
# button2 = KeyboardButton("Информация")
# kb.add(button)
# kb.add(button2)

ikb = InlineKeyboardMarkup()
button = InlineKeyboardButton("Рассчитать норму калорий", callback_data="calories")
button2 = InlineKeyboardButton("Формулы расчёта", callback_data="info")
ikb.add(button)
ikb.add(button2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


api = ONLY_MY_API
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выбери опцию:", reply_markup=ikb)


@dp.callback_query_handler(text="info")
async def get_formulas(call):
    await call.message.answer(" Упрощенный вариант формулы Миффлина-Сан Жеора:\n"
                              "для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;\n"
                              "для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.")
    await call.answer()


@dp.message_handler(commands="start")
async def start(message: types.Message):
    await message.answer('Привет, я бот помогающий твоему здоровью!', reply_markup=kb)


@dp.message_handler(text="Информация")
async def send_info(message):
    await message.answer("Бот помогает рассчитать количество калорий,"
                         " которые нужно потреблять в день,"
                         " чтобы поддерживать свой вес."
                         " Для этого введите ваш возраст, рост и вес.")


@dp.message_handler(text="Рассчитать калории")
async def set_age(message):
    await message.answer("Введите ваш возраст:")
    await UserState.age.set()


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите ваш возраст:")
    await UserState.age.set()
    await call.answer()


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
