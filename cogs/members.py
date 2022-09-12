import discord
import sys
sys.path.append("..")

from discord.ext import commands
from discord.ext.commands import errors
import asyncio
from db import db


class MembersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='spy')
    @commands.guild_only()
    async def spy(self, ctx: commands.Context, *, member: discord.Member):
        _db = db.Database(member.guild.id)
        _db.add_user_to_spy_table(member.id)
        _db.set_alarm_channel(ctx.message.channel.id)
        _db.close()
        await ctx.send(f'{member.display_name} взят под наблюдение')

    @commands.command(name='despy')
    @commands.guild_only()
    async def despy(self, ctx, *, member: discord.Member):
        _db = db.Database(member.guild.id)
        _db.remove_user_from_spy(member.id)
        _db.close()
        await ctx.send(f'{member.display_name} больше не под наблюдением')

    @commands.Cog.listener()
    async def on_presence_update(self, before: discord.Member, after: discord.Member):
        _db = db.Database(after.guild.id)
        if _db.check_spy_user(after.id):
            await self.bot.get_channel(_db.get_alarm_channel()).send(f"@everyone ALLARM! <@{after.id}> В СЕТИ")
        _db.close()

async def setup(bot):
    await bot.add_cog(MembersCog(bot))