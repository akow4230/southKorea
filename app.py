import asyncio
from aiogram import executor
from loader import dp, db
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from handlers.users.allPositions import sendAllPositions, sendNewPositions  # Import sendAllPositions
from environs import Env
from apscheduler.schedulers.asyncio import AsyncIOScheduler

env = Env()
env.read_env()  # Load environment variables from .env

scheduler = None  # Initialize scheduler as a global variable

async def on_startup(dispatcher):
    global scheduler
    scheduler = AsyncIOScheduler()
    await db.create()
    await db.create_table_users()
    await db.create_table_admins()
    await db.create_table_time()
    await db.create_table_status()
    await db.create_table_channelpost()
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    await db.create_table_trader_orders()

    scheduler.add_job(sendAllPositions, 'interval', seconds=5)
    scheduler.add_job(sendNewPositions, 'interval', seconds=5)
    scheduler.start()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

