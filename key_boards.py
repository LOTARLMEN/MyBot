from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton("Рассчитать калории"),
               KeyboardButton("Информация")],
              [KeyboardButton("Купить"), ]],
    resize_keyboard=True)

ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        InlineKeyboardButton("Рассчитать норму калорий", callback_data="calories"),
        InlineKeyboardButton("Формулы расчёта", callback_data="info")
    ],
    resize_keyboard=True)

ikb2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Product1", callback_data="product_buying"),
         InlineKeyboardButton("Product2", callback_data="product_buying"),
         InlineKeyboardButton("Product3", callback_data="product_buying"),
         InlineKeyboardButton("Product4", callback_data="product_buying")]
    ],
    resize_keyboard=True)
