from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config

class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS botusers (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE 
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO botusers (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM botusers"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM botusers WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM botusers"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE botusers SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM botusers WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE botusers", execute=True)



    #   ADMIN TABLE

    async def create_table_admins(self):
        sql = """
        CREATE TABLE IF NOT EXISTS admins (
            adminid BIGINT NOT NULL UNIQUE,
            adminname VARCHAR(255) NOT NULL           
        );
        """
        await self.execute(sql, execute=True)

    async def add_admin(self, adminid, adminname):
        sql = "INSERT INTO admins (adminid, adminname) VALUES($1, $2) returning *"
        return await self.execute(sql, adminid, adminname, fetchrow=True)

    async def select_admin(self, **kwargs):
        sql = "SELECT * FROM admins WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)



    # TIME INTERVAL

    async def create_table_time(self):
        sql = """
           CREATE TABLE IF NOT EXISTS time_interval (
                id SERIAL PRIMARY KEY,
                time Integer NOT NULL           
           );
           """
        await self.execute(sql, execute=True)


    async def update_time(self, time):
        sql = "UPDATE time_interval SET time=$1 WHERE id=1"
        return await self.execute(sql, time, execute=True)

    async def select_time(self, **kwargs):
        sql = "SELECT * FROM time_interval WHERE id=1"
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)



    # Database functions for bot status

    async def create_table_status(self):
        sql = """
              CREATE TABLE IF NOT EXISTS bot_status (
                   id SERIAL PRIMARY KEY,
                   status Boolean NOT NULL           
              );
              """
        await self.execute(sql, execute=True)

    async def update_status(self, status):
        sql = "UPDATE bot_status SET status=$1 WHERE id=1"
        return await self.execute(sql, status, execute=True)

    async def select_status(self, **kwargs):
        sql = "SELECT * FROM bot_status WHERE id=1 "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)


    # TRADERS

    async def create_table_traders(self):
        sql = """
        CREATE TABLE IF NOT EXISTS traders (
        Uid VARCHAR(255) NOT NULL,
        tradername VARCHAR(255) NOT NULL,
        traderpositions VARCHAR(20000) NULL,
        Pnl_trade INT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def select_uid_name_list(self):
        sql = "SELECT Uid, tradername FROM traders"  # Select both UID and trader name
        rows = await self.execute(sql, fetch=True)
        print("Fetched rows:", rows)  # Print fetched rows for debugging
        uid_name_list = [(row['uid'], row['tradername']) for row in rows]  # Extract both UID and trader name
        return uid_name_list

    async def select_trader_positions(self):
        sql = "SELECT Uid, tradername, TraderPositions, Pnl_trade FROM traders"
        return await self.execute(sql, fetch=True)

    async def select_trader_by_uid(self, uid):
        sql = "SELECT * FROM traders WHERE Uid = $1"
        return await self.execute(sql, uid, fetchrow=True)

    async def delete_traders(self, Uid):
        sql = "DELETE FROM traders WHERE Uid=$1"
        return await self.execute(sql, Uid, fetchrow=True)

    async def drop_traders(self):
        await self.execute("DROP TABLE traders", execute=True)


#   TRADER ORDERS

    async def create_table_trader_orders(self):
        sql = """
        CREATE TABLE IF NOT EXISTS trader_orders (
            id UUID PRIMARY KEY,
            uid VARCHAR(255),
            name VARCHAR(255),
            symbol VARCHAR(255),
            entry_price FLOAT,
            mark_price FLOAT,
            pnl FLOAT,
            roe FLOAT,
            amount FLOAT,
            update_timestamp BIGINT,
            trade_before BOOLEAN,
            is_long BOOLEAN,
            is_short BOOLEAN,
            leverage FLOAT
        );
        """
        await self.execute(sql, execute=True)

    # In your database module (loader.py or db.py)

    async def select_trader_orders_by_uid(self, uid):
        sql = "SELECT * FROM trader_orders WHERE uid = $1"
        return await self.execute(sql, uid, fetch=True)

    async def delete_trader_orders_by_uid(self, uid: str):
        sql = "DELETE FROM trader_orders WHERE uid = $1"
        async with self.pool.acquire() as connection:
            await connection.execute(sql, uid)


    # CHANNEL POST
    async def create_table_channelpost(self):
        sql = """
        CREATE TABLE IF NOT EXISTS channelpost (
            id SERIAL PRIMARY KEY,
            traderuid VARCHAR(255) NOT NULL,
            tradetype VARCHAR(255) NOT NULL,  -- Corrected variable name
            coinName VARCHAR(255) NOT NULL,
            side VARCHAR(255) NOT NULL,
            leverage FLOAT NOT NULL,
            entryPrice FLOAT NOT NULL,
            marketPrice FLOAT NOT NULL,
            reo_position FLOAT NOT NULL,
            amount_position FLOAT NOT NULL,
            pnl FLOAT NOT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def add_channelpost(self, traderuid, tradetype, coinName, side, leverage, entryPrice, marketPrice,
                              reo_position, amount_position, pnl):
        sql = """
        INSERT INTO channelpost (traderuid, tradetype, coinName, side, leverage, entryPrice, marketPrice, reo_position, amount_position, pnl)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        RETURNING *;
        """
        return await self.execute(sql, traderuid, tradetype, coinName, side, leverage, entryPrice, marketPrice,
                                  reo_position, amount_position, pnl, fetchrow=True)

    async def select_channelposts(self):
        sql = "SELECT * FROM channelpost"
        return await self.execute(sql, fetch=True)

    async def delete_id(self, id: str):
        sql = "DELETE FROM channelpost WHERE id = $1"
        async with self.pool.acquire() as connection:
            await connection.execute(sql, id)
