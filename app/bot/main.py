import asyncio

from aiogram import Bot, Dispatcher

from app.bot.handlers import orders, start, stars, tickets
from app.config import settings
from app.database import init_db


async def run_bot() -> None:
    init_db()
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(orders.router)
    dp.include_router(stars.router)
    dp.include_router(tickets.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_bot())
