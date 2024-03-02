from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from aiogram.client.session.aiohttp import AiohttpSession
from config_reader import config
from models import Data
from validation import Validator
from typing import Optional
import asyncio
import logging


logging.basicConfig(level=logging.INFO)
session = AiohttpSession(proxy=config.proxy_server.get_secret_value())
bot = Bot(token=config.bot_token.get_secret_value(), session=session)
dp = Dispatcher()
data = Data()

def get_yandex_token(command: CommandObject) -> Optional[str]:
    try:
        Validator.validate_add_token_command(command)
        return command.args.split(" ", maxsplit=1)[0]
    except ValueError:
        raise RuntimeError(
            "Error: wrong command format. Example:\n"
            f"/{command.command} <token>"
        )

@dp.message(Command("add_yandex_token"))
async def cmd_add_yandex_token(message: types.Message, command: CommandObject) -> None:
    try:
        Validator.validate_message(message)
        yandex_token = get_yandex_token(command)
        data.save_yandex_token(message.from_user.username, yandex_token)
    except Exception as ex:
        await message.answer(str(ex))
        return

    await message.answer("Yandex token added successfully!\n")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    try:
        Validator.validate_message(message)
        data.create_user(message.from_user.username)
    except Exception as ex:
        await message.answer(str(ex))
        return

    await message.answer("Register success!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
