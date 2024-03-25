import asyncio
import json
from aiogram import types
from loader import dp, db

from datetime import datetime

async def sendAllPositions():
    bot_status = await db.select_status()
    if bot_status['status']:
        # await dp.bot.send_message(chat_id=-1002025769840, text="================")
        uid_name_list = await db.select_uid_name_list()
        for uid, trader_name in uid_name_list:
            trader_orders = await db.select_trader_orders_by_uid(uid)

            current_time = datetime.now().strftime('%d.%m.%Y, %I:%M %p')
            message_text = (f"<b>🥷🏾 | Trader : </b> {trader_name} \n"
                            f"<b>⏰ | Current Time: </b> {current_time}\n"
                            f"———————————————\n")

            if len(trader_orders) == 0:
                message_text += "<b>No trade</b>\n"
            else:
                for order in trader_orders:
                    message_text += (
                        f"<b>🪙 | Crypto:</b> {order['symbol']}\n"
                        f"<b>🚀 | Leverage:</b> {order['leverage']}\n"
                        f"<b>{'🟢 | Trade: LONG' if order['is_long'] else '🔴 | Trade: SHORT'}</b>\n"
                        f"<b>📊 | Entry price:</b> {round(float(order['entry_price']), 4)}\n"
                        f"<b>📈 | Market Price:</b> {round(float(order['mark_price']), 4)}\n"
                        f"<b>💰 | Size:</b> {order['amount']}\n"
                        f"<b>💵 | PNL:</b> {round(float(order['pnl']), 4)} USDT\n"
                        f"<b>🧮 | Roe:</b> {round(float(order['roe'])*100, 4)} %\n"
                        f"———————————————\n"
                    )

                try:
                    await dp.bot.send_message(chat_id=-1002025769840, text=message_text)
                    await db.delete_trader_orders_by_uid(uid)
                except Exception as e:
                    await db.delete_trader_orders_by_uid(uid)
                    print(f"An error occurred while sending message to the channel: {e}")


async def sendNewPositions():
    bot_status = await db.select_status()
    orders = await db.select_channelposts()
    if bot_status['status']:
        for order in orders:
            trader = await db.select_trader_by_uid(order['traderuid'])
            if order['tradetype'] == 'OPENED':
                await dp.bot.send_message(chat_id=-1002005180992,
                                          text=f"<b>🔔 | OPEN TRADE ALERT</b>\n\n"
                                               f"<b>🥷 | Trader:</b> {trader['tradername']}\n"
                                               f"<b>🪙 | Crypto:</b> {order['coin_name']}\n\n"
                                               f"<b>🚀 | Leverage:</b> {order['leverage']}\n"
                                               f"<b>{'🟢 | Trade: LONG' if order['side']=='buy' else '🔴 | Trade: SHORT'}</b>\n"
                                               f"<b>📊 | Entry price:</b> {round(float(order['entry_price']), 4)}\n"
                                               f"<b>💰 | Size:</b> {order['amount_position']}$\n"
                                               f"<b>💵 | PNL:</b> {round(float(order['pnl']), 4)} USDT\n"
                                               f"<b>🧮 | Roe:</b> {round(float(order['reo_position']) * 100, 4)} %\n"
                                          )
                await asyncio.sleep(1)
            else:
                await dp.bot.send_message(chat_id=-1002005180992,
                                          text=f"<b>🔴 | TRADE CLOSED</b>\n\n"
                                               f"<b>🥷 | Trader:</b> {trader['tradername']}\n"
                                               f"<b>🪙 | Crypto:</b> {order['coin_name']}\n\n"
                                               f"<b>🚀 | Leverage:</b> {order['leverage']}\n"
                                               f"<b>{'🟢 | Trade: LONG' if order['side'] == 'buy' else '🔴 | Trade: SHORT'}</b>\n"
                                               f"<b>📊 | Entry price:</b> {round(float(order['entry_price']), 4)}\n"
                                               f"<b>📈 | Market Price:</b> {round(float(order['market_price']), 4)}\n"
                                               f"<b>💵 | PNL:</b> {round(float(order['pnl']), 4)} USDT\n"
                                               f"<b>🧮 | Roe:</b> {round(float(order['reo_position'])*100, 4)} %\n"
                                          )
                await asyncio.sleep(1)
            await db.delete_id(order['id'])