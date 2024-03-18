import aiogram
import asyncpg
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, db, bot
from data.config import ADMINS
from aiogram.types import WebAppInfo



# Function to retrieve the bot status from the database
async def get_bot_status():
    result = await db.select_status()
    return result['status']

@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    is_admin = await db.select_admin(adminid=message.from_user.id)
    if is_admin:
        # Get the bot status from the database
        current_status = await get_bot_status()
        text = "ON🟢" if current_status else "OFF🟢"

        markup = InlineKeyboardMarkup(row_width=1)
        new_button = InlineKeyboardButton('🤖 BOT: '+text, callback_data='botStatus')
        markup.add(new_button)

        web_app_button = types.KeyboardButton('📈 Traders 📈')
        web_app_info = WebAppInfo(url='https://cryptoz.fun/newtraders')
        web_app_button.web_app = web_app_info
        markup.add(web_app_button)
        time = await db.select_time()
        time_button = InlineKeyboardButton(f"⌚️Time interval: {time['time']}", callback_data='time')
        markup.add(time_button)
        await message.answer("<b>Use the buttons below to easily manage your bot and trades:</b>", reply_markup=markup)
        return


    is_user = await db.select_user(telegram_id=message.from_user.id)
    if is_user:
        # Send a greeting message to existing users
        await message.answer("Hi👋!")
    else:
        try:
            # Add the user to the database
            user = await db.add_user(
                telegram_id=message.from_user.id,
                full_name=message.from_user.full_name,
                username=message.from_user.username
            )
        except asyncpg.exceptions.UniqueViolationError:
            # If the user is already in the database, send a welcome message
            await message.answer("Welcome!")
            user = await db.select_user(telegram_id=message.from_user.id)

        # Send a welcome message
        await message.answer("Welcome!")

        # Notify admins
        count = await db.count_users()
        msg = f"{user[1]} {from_user.username} joined the platform.\nTotal users: {count}"
        await bot.send_message(chat_id=ADMINS[0], text=msg)

@dp.callback_query_handler(lambda query: query.data == 'botStatus')
async def toggle_bot_status(callback_query: types.CallbackQuery):
    current_status = await get_bot_status()
    new_status = not current_status
    await db.update_status(new_status)

    text = "ON🟢" if new_status else "OFF🟢"
    new_button = InlineKeyboardButton('🤖 BOT: ' + text, callback_data='botStatus')

    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(new_button)

    web_app_button = types.KeyboardButton('📈 Traders 📈')
    web_app_info = types.WebAppInfo(url='https://cryptoz.fun/newtraders')
    web_app_button.web_app = web_app_info
    markup.add(web_app_button)

    time = await db.select_time()
    time_button = InlineKeyboardButton(f"⌚️Time interval: {time['time']}", callback_data='time')
    markup.add(time_button)

    try:
        await callback_query.message.edit_reply_markup(reply_markup=markup)
    except aiogram.utils.exceptions.MessageNotModified:
        chat_id = callback_query.message.chat.id
        message_id = callback_query.message.message_id

        try:
            await bot.delete_message(chat_id, message_id)
        except aiogram.utils.exceptions.MessageToDeleteNotFound:
            pass
        await callback_query.message.answer("<b>Use the buttons below to easily manage your bot and trades:</b>", reply_markup=markup)
