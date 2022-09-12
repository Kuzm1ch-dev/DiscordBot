from dis import dis, disco
import imp
import discord
import sys
sys.path.append("..")

from discord.ext import commands
from discord.ext.commands import errors
import asyncio
from db import db


class EventCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

async def setup(bot):
    await bot.add_cog(EventCog(bot))