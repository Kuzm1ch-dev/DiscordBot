from email.mime import application
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound, RoleNotFound, MemberNotFound
import discord

import asyncio
import os
import aiohttp

from dotenv import load_dotenv
from db import db


load_dotenv()


intents = discord.Intents.all()

def get_prefix(bot, message):

    # Доступные префиксы
    prefixes = ['.', '!', '?', '-']

    # Проверка на сообщения не из гильдии
    if not message.guild:
        return '?'

    #Возвращаем доступные префиксы
    return commands.when_mentioned_or(*prefixes)(bot, message)

class ExBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=get_prefix, description='Мяу!', intents=intents, case_insensitive=True)
        self.initial_extensions =[
            'cogs.members',
            'cogs.events'
        ]
    
    async def setup_hook(self)-> None:

        self.background_task.start()
        self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            await self.load_extension(ext)
            print(f"Расширение {ext} загружено ")

        await bot.tree.sync()

    async def close(self):
        await super().close()
        await self.session.close()

    @tasks.loop(seconds=60)
    async def background_task(self):
        print('Запуск фоновых задач...')


bot = ExBot()
bot.remove_command("help")

if __name__ == "__main__":
    bot.run(os.getenv('TOKEN'), reconnect=True)