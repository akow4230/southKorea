import asyncio
from aiogram import types, executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from loader import dp, db
from environs import Env
from apscheduler.schedulers.asyncio import AsyncIOScheduler

env = Env()
env.read_env()  # Load environment variables from .env

PASSWORD = "12345678"


async def get_bot_status():
    result = await db.select_status()
    return result['status']



@dp.message_handler(commands=['password'])
async def check_password(message: types.Message):
    password_attempt = message.get_args()
    is_admin = await db.select_admin(adminid=message.from_user.id)
    if is_admin:
        current_status = await get_bot_status()
        text = "ON🟢" if current_status else "OFF🟢"

        markup = InlineKeyboardMarkup(row_width=1)

        new_button = InlineKeyboardButton('🤖 BOT: ' + text, callback_data='botStatus')
        markup.add(new_button)

        web_app_button = types.KeyboardButton('📈 Traders ')
        web_app_info = WebAppInfo(url='https://cryptoz.fun/newtraders')
        web_app_button.web_app = web_app_info
        markup.add(web_app_button)

        time = await db.select_time()
        time_button = InlineKeyboardButton(f"⌚️Time interval: {time['time']}", callback_data='time')
        markup.add(time_button)
        await message.answer("<b>Use the buttons below to easily manage your bot and trades:</b>", reply_markup=markup)
        return
    if password_attempt == PASSWORD:
        await db.add_admin(adminid=message.from_user.id, adminname=message.from_user.username)
        await message.answer("Password correct!")

        current_status = await get_bot_status()
        text = "ON🟢" if current_status else "OFF🟢"

        markup = InlineKeyboardMarkup(row_width=1)

        new_button = InlineKeyboardButton('🤖 BOT: ' + text, callback_data='botStatus')
        markup.add(new_button)

        web_app_button = types.KeyboardButton('📈 Traders ')
        web_app_info = WebAppInfo(url='https://cryptoz.fun/newtraders')
        web_app_button.web_app = web_app_info
        markup.add(web_app_button)
        time = await db.select_time()
        time_button = InlineKeyboardButton(f"⌚️Time interval: {time['time']}", callback_data='time')
        markup.add(time_button)
        await message.answer("<b>Use the buttons below to easily manage your bot and trades:</b>", reply_markup=markup)
        return;
    else:
        await message.answer("Incorrect password. Please try again.")


@dp.message_handler(commands=['time'])
async def update_time_interval(message: types.Message):
    is_admin = await db.select_admin(adminid=message.from_user.id)
    if is_admin:
        new_time = message.get_args()
        if int(new_time)>9:
            try:
                await db.update_time(int(new_time))
                await message.reply("Time interval updated successfully!")
                current_status = await get_bot_status()
                text = "ON🟢" if current_status else "OFF🟢"

                markup = InlineKeyboardMarkup(row_width=1)

                new_button = InlineKeyboardButton('🤖 BOT: ' + text, callback_data='botStatus')
                markup.add(new_button)

                web_app_button = types.KeyboardButton('📈 Traders ')
                web_app_info = WebAppInfo(url='https://cryptoz.fun/newtraders')
                web_app_button.web_app = web_app_info
                markup.add(web_app_button)
                time = await db.select_time()
                time_button = InlineKeyboardButton(f"⌚️Time interval: {time['time']}", callback_data='time')
                markup.add(time_button)
                await message.answer("<b>Use the buttons below to easily manage your bot and trades:</b>",
                                     reply_markup=markup)

            except Exception as e:
                await message.reply(f"An error occurred while updating the time interval: {e}")
        else:
            await message.reply("Please enter a new time interval value, maximum 10 seconds.")
    else:
        await message.reply("You are not authorized to update the time interval.")

