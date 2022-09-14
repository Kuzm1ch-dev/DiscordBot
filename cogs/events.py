import discord
import sys
sys.path.append("..")

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import errors
import asyncio
from db import db


async def load_database(bot):
    if db.Database.check_database() == False:
        db.Database.create_database()
    
    for guild in bot.guilds:
        _db = db.Database(guild.id)
        _db.check_tables()
        _db.close()
    
    _db.close()


class EventCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'\n\nЗашел как: {self.bot.user.name} - {self.bot.user.id}\nВерсия: {discord.__version__}\n')
        await load_database(self.bot)
        # Меняем статус бота
        await self.bot.change_presence(activity=discord.Game(name='рабочинские прибаутки', type=1, url='https://vk.com/kuzm14'))
        print(f'Успешно авторизован и запущен...!')

    @commands.Cog.listener()
    async def on_presence_update(self, before: discord.Member, after: discord.Member):
        _db = db.Database(after.guild.id)
        if _db.check_spy_user(after.id):
            await self.bot.get_channel(_db.get_alarm_channel()).send(f"@everyone ВНИМАНИЕ! <@{after.id}> В СЕТИ")
        _db.close()
    
async def setup(bot):
    await bot.add_cog(EventCog(bot))