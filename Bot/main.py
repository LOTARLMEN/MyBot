from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from my_api import ONLY_MY_API
import asyncio



api = ONLY_MY_API
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    print('Нам написали /start!')
    await message.answer('Привет!Я бот помогающий твоему здоровью!')



@dp.message_handler()
async def all_messages(message: types.Message):
        print('Нам написали что-то кроме /start!')
        await message.answer('Введите команду /start чтобы начать общение!')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)