from aiogram import types
from aiogram.types import WebAppInfo
from aiogram.types import ContentType
from loader import dp
import requests



@dp.message_handler(commands=['weather'])
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # Create a reply keyboard markup
    web_app_button = types.KeyboardButton('teast javascript')
    web_app_info = WebAppInfo(url='https://muhiuchun.netlify.app/')
    web_app_button.web_app = web_app_info

    web_app_button_ru = types.KeyboardButton('React')
    web_app_info_ru = WebAppInfo(url='https://65b459a1b7d1d8388d756cce--p0apaya-torrone-b9eb00.netlify.app/userform')
    # web_app_info_ru = WebAppInfo(url='https://6577c5779e5338747637b404--lucky-rugelach-cf0e40.netlify.app/')
    web_app_button_ru.web_app = web_app_info_ru

    markup.add(web_app_button_ru)
    markup.add(web_app_button)
    await message.reply("Enter event details:", reply_markup=markup)

@dp.message_handler(commands=['startjon'])
async def start(message: types.Message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    str
    web_app_button = types.InlineKeyboardButton(text='Uz',  web_app=WebAppInfo(url=f'https://akobir.co/image'))
    # web_app_button1 = types.InlineKeyboardButton(text='Ru',  url=f'https://kun.uz/')
    markup.add(web_app_button)
    # markup.add(web_app_button1)
    await message.reply("Click the button to open the web app:", reply_markup=markup)
@dp.message_handler(content_types=['web_app_data'])
async def web_app(message: types.Message):
    print(message.web_app_data.data)
    try:
        await message.answer(message.web_app_data.data)

    except Exception as e:
        await message.answer(f"Error: {e}")
# @dp.message_handler(commands=['startjon'])
# async def start(message: types.Message):
#     markup = types.InlineKeyboardMarkup()
#     web_app_button = types.InlineKeyboardButton(text='Uz',  web_app=WebAppInfo(url=f'https://dynamic-daffodil-aeb0a9.netlify.app/'))
#     web_app_button1 = types.InlineKeyboardButton(text='Ru',  web_app=WebAppInfo(url=f'https://prismatic-pegasus-aca2f3.netlify.app/'))
#     markup.add(web_app_button)
#     markup.add(web_app_button1)
#     await message.reply("Click the button to open the web app:", reply_markup=markup)
#
# @dp.message_handler(content_types=['web_app_data'])
# async def web_app(message: types.Message):
#     print(message.web_app_data.data)
#     try:
#         await message.answer(message.web_app_data.data)
#
#     except Exception as e:
#         await message.answer(f"Error: {e}")


# Echo bot
# @dp.message_handler(state=None)
# async def bot_echo(message: types.Message):
#     await message.answer(message.text+"\n nima gap!")
#
