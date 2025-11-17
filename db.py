# db.py
import os
import json
import asyncio

# choose backend: if DATABASE_URL set -> postgres (asyncpg), else SQLite (aiosqlite)
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    import asyncpg
else:
    import aiosqlite

class DB:
    def __init__(self):
        self.pool = None
        self.sqlite_conn = None
        self.is_postgres = bool(DATABASE_URL)

    async def connect(self):
        if self.is_postgres:
            self.pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=3)
        else:
            # use local sqlite file
            self.sqlite_conn = await aiosqlite.connect("data/game.db")
            # enable WAL for concurrency
            await self.sqlite_conn.execute("PRAGMA journal_mode=WAL;")
            await self.sqlite_conn.commit()

    async def close(self):
        if self.is_postgres and self.pool:
            await self.pool.close()
        if self.sqlite_conn:
            await self.sqlite_conn.close()

    # init tables (simple players and world)
    async def init_tables(self):
        if self.is_postgres:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    user_id TEXT PRIMARY KEY,
                    data JSONB NOT NULL
                );
                """)
                await conn.execute("""
                CREATE TABLE IF NOT EXISTS world (
                    key TEXT PRIMARY KEY,
                    data JSONB NOT NULL
                );
                """)
        else:
            await self.sqlite_conn.execute("""
            CREATE TABLE IF NOT EXISTS players (
                user_id TEXT PRIMARY KEY,
                data TEXT NOT NULL
            );
            """)
            await self.sqlite_conn.execute("""
            CREATE TABLE IF NOT EXISTS world (
                key TEXT PRIMARY KEY,
                data TEXT NOT NULL
            );
            """)
            await self.sqlite_conn.commit()

    # player helpers
    async def get_player(self, user_id):
        if self.is_postgres:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow("SELECT data FROM players WHERE user_id=$1", str(user_id))
                return dict(row["data"]) if row else None
        else:
            cur = await self.sqlite_conn.execute("SELECT data FROM players WHERE user_id=?", (str(user_id),))
            row = await cur.fetchone()
            await cur.close()
            return json.loads(row[0]) if row else None

    async def upsert_player(self, user_id, data: dict):
        if self.is_postgres:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                INSERT INTO players(user_id, data) VALUES($1, $2)
                ON CONFLICT (user_id) DO UPDATE SET data = EXCLUDED.data
                """, str(user_id), data)
        else:
            text = json.dumps(data, ensure_ascii=False)
            await self.sqlite_conn.execute("""
            INSERT INTO players(user_id, data) VALUES(?, ?)
            ON CONFLICT(user_id) DO UPDATE SET data=excluded.data;
            """, (str(user_id), text))
            await self.sqlite_conn.commit()

    async def delete_player(self, user_id):
        if self.is_postgres:
            async with self.pool.acquire() as conn:
                await conn.execute("DELETE FROM players WHERE user_id=$1", str(user_id))
        else:
            await self.sqlite_conn.execute("DELETE FROM players WHERE user_id=?", (str(user_id),))
            await self.sqlite_conn.commit()

    # world helpers (simple key-value)
    async def get_world(self, key):
        if self.is_postgres:
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow("SELECT data FROM world WHERE key=$1", str(key))
                return dict(row["data"]) if row else None
        else:
            cur = await self.sqlite_conn.execute("SELECT data FROM world WHERE key=?", (str(key),))
            row = await cur.fetchone()
            await cur.close()
            return json.loads(row[0]) if row else None

    async def upsert_world(self, key, data: dict):
        if self.is_postgres:
            async with self.pool.acquire() as conn:
                await conn.execute("""
                INSERT INTO world(key, data) VALUES($1, $2)
                ON CONFLICT (key) DO UPDATE SET data = EXCLUDED.data
                """, str(key), data)
        else:
            text = json.dumps(data, ensure_ascii=False)
            await self.sqlite_conn.execute("""
            INSERT INTO world(key, data) VALUES(?, ?)
            ON CONFLICT(key) DO UPDATE SET data=excluded.data;
            """, (str(key), text))
            await self.sqlite_conn.commit()

# single global instance
_db = DB()

async def connect_db():
    await _db.connect()
    await _db.init_tables()

async def close_db():
    await _db.close()

def get_db():
    return _db
