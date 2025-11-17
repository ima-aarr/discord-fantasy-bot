# migrate.py
import asyncio
from db import connect_db, close_db, get_db

async def main():
    await connect_db()
    # tables are created in connect_db->init_tables
    print("DB initialized")
    await close_db()

if __name__ == "__main__":
    asyncio.run(main())
