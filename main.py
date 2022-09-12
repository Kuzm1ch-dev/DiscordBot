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
            'cogs.members'
        ]
    
    async def setup_hook(self)-> None:
        self.background_task.start()
        self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            await self.load_extension(ext)
            print(f"Расширение {ext} загружено ")

    async def close(self):
        await super().close()
        await self.session.close()

    @tasks.loop(seconds=60)
    async def background_task(self):
        print('Запуск фоновых задач...')
    

    async def on_ready(self):
        print('Запущен!')

bot = ExBot()
bot.remove_command("help")

async def load_database():
    if db.Database.check_database() == False:
        db.Database.create_database()
    
    for guild in bot.guilds:
        _db = db.Database(guild.id)
        _db.check_tables()
        _db.close()
    
    _db.close()

@bot.event
async def on_ready():
    print(f'\n\nЗашел как: {bot.user.name} - {bot.user.id}\nВерсия: {discord.__version__}\n')
    await load_database()
    # Меняем статус бота
    await bot.change_presence(activity=discord.Game(name='рабочинские прибаутки', type=1, url='https://vk.com/kuzm14'))
    print(f'Успешно авторизован и запущен...!')


if __name__ == "__main__":
    bot.run(os.getenv('TOKEN'), reconnect=True)