from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ContentType
from core.handlers.basic import get_start, get_photo, get_hello
import asyncio
import logging
from core.settings import settings
from aiogram.filters import Command
from core.filters.is_contact import IsTrueContact
from core.handlers.contact import get_true_contact, get_fake_contact


async def start_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот запущен')

async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот остановлен')

async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')

    dp = Dispatcher()
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_photo, F.photo)
    dp.message.register(get_hello, F.text == 'Привет')
    dp.message.register(get_start, Command(commands=['start', 'run']))
    dp.message.register(get_true_contact, F.contact, IsTrueContact())
    dp.message.register(get_fake_contact, F.contact)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(start())