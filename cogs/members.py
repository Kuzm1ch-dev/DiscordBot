from dis import disco
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
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="command-1")
    async def my_command(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("Hello from command 1!", ephemeral=True)


    @app_commands.command(name='spy')
    @app_commands.guild_only()
    async def spy(self, interaction: discord.Interaction, *, member: discord.Member):
        _db = db.Database(member.guild.id)
        if (_db.check_alarm_channel() == False):
            await interaction.response.send_message(f'Канал оповещений не назначен, воспользуйтесь коммандой \'/setalarm\'')
            _db.close()
            return
        if (_db.check_spy_user(member.id)):
            await interaction.response.send_message(f'{member.display_name} уже под наблюдением') 
            _db.close()
            return 
        _db.add_user_to_spy_table(member.id)
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
    async def getalarm(self, interaction: discord.Interaction):
        _db = db.Database(interaction.guild_id)
        if (_db.check_alarm_channel()):
            await interaction.response.send_message(f'Канал оповещений: {_db.get_alarm_channel()}')
        else:
            await interaction.response.send_message(f'Канал оповещений не назначен, воспользуйтесь коммандой \'/setalarm\'')
        _db.close()

    @app_commands.command(name='setalarm')
    @app_commands.guild_only()
    async def setalarm(self, interaction: discord.Interaction):
        _db = db.Database(interaction.guild_id)
        _db.set_alarm_channel(interaction.channel_id)   
        await interaction.response.send_message(f'Канал {interaction.channel.name} теперь используется для оповеений')
        _db.close()

    @app_commands.command(name='remalarm')
    @app_commands.guild_only()
    async def remalarm(self, interaction: discord.Interaction):
        _db = db.Database(interaction.guild_id)
        _db.remove_alarm_channel()   
        await interaction.response.send_message(f'Канал оповещений удален! Чтобы назначить новый, воспользуйтесь коммандой \'/setalarm\'')
        _db.close()

async def setup(bot):
    await bot.add_cog(MembersCog(bot))