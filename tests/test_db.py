import asyncio
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine

from src.databae.models import *
from src.config.config import config

engine = create_async_engine(config.DATABASE_URL, echo=True)


async def test():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    print("Таблицы успешно созданы ✅")


asyncio.run(test())
