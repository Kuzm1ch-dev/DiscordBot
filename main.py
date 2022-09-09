from ast import Pass
from cmath import log
from dis import dis, disco
from unittest import async_case
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound, RoleNotFound, MemberNotFound
import discord

import asyncio
import os
import aiohttp
from os import listdir
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
            'cogs.simple'
        ]
    
    async def setup_hook(self):
        self.background_task.start()
        self.session = aiohttp.ClientSession()
        for ext in self.initial_extensions:
            await self.load_extension(ext)
    async def close(self):
        await super().close()
        await self.session.close()

    @tasks.loop(minutes=10)
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

        # Проверяем таблицу уровней, все ли роли уровней созданы
        for level in _db.get_level_pattern():
            print (level)
            if (level[5] == None or level[5] == ""): # Если роль новая, то создать ее на сервере
                print(f"На сервере {guild.id} найдена новая роль {level[1]}")
                role = await guild.create_role(name = f"{level[1]}", color=discord.Color.from_rgb(*level[2:5]))
                print(f"На сервере {guild.id} создана роль {role.name}")
                _db.update_roleid_on_table(level[0],role.id)

        # Проверка, есть ли новые пользователи
        for member in guild.members:
            query = _db.check_newbie_user(uid= member.id)
            if query != None:
                await member.add_roles(guild.get_role(int(query)))

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

