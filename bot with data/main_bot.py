import asyncio
import logging
from aiogram import Bot, Dispatcher

from configuration import config
from handlers import notes

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


async def main()-> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    dp.include_router(notes.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped.")

