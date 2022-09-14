from imaplib import Commands
from tkinter.tix import Tree
import discord
import sys
sys.path.append("..")

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import errors
import asyncio
from db import db



class MembersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @app_commands.command(name="command-1")
    async def my_command(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Hello from command 1!", ephemeral=True)


    @app_commands.command(name='spy')
    @app_commands.guild_only()
    async def spy(self, interaction: discord.Interaction, *, member: discord.Member):
        _db = db.Database(member.guild.id)
        _db.add_user_to_spy_table(member.id)
        _db.set_alarm_channel(interaction.channel_id)
        _db.close()
        await interaction.response.send_message(f'{member.display_name} взят под наблюдение')

    @app_commands.command(name='despy')
    @app_commands.guild_only()
    async def despy(self, interaction: discord.Interaction, *, member: discord.Member):
        _db = db.Database(member.guild.id)
        _db.remove_user_from_spy(member.id)
        _db.close()
        await interaction.response.send_message(f'{member.display_name} больше не под наблюдением')

    @app_commands.command(name='alarm')
    @app_commands.guild_only()
    async def despy(self, interaction: discord.Interaction):
        print(interaction.guild_id)
        _db = db.Database(interaction.guild_id)
        await interaction.response.send_message(f'Алярм канал: {_db.get_alarm_channel()}')
        _db.close()

    @commands.Cog.listener()
    async def on_presence_update(self, before: discord.Member, after: discord.Member):
        _db = db.Database(after.guild.id)
        if _db.check_spy_user(after.id):
            await self.bot.get_channel(_db.get_alarm_channel()).send(f"@everyone ALARM! <@{after.id}> В СЕТИ")
        _db.close()

async def setup(bot):
    await bot.add_cog(MembersCog(bot))