from dis import dis, disco
import imp
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

    @commands.command(name='respect', aliases=['res'])
    @commands.guild_only()
    async def respect(self, ctx, *, member: discord.Member=None):
        if member is None or member == ctx.author:
            return

        _db = db.Database(member.guild.id)
        if _db.add_exp(member.id, 500): # Если уровень повысился, меняем роль
            role = member.guild.get_role(int(_db.requeried_roleid( _db.get_level(member.id))))
            await member.edit(roles=[role])
        _db.close()
        await ctx.send(f'Респект плотный тебе, <@{member.id}>')
            
    @commands.command()
    @commands.guild_only()
    async def joined(self, ctx, *, member: discord.Member):
        """Says when a member joined."""
        await ctx.send(f'{member.display_name} joined on {member.joined_at}')

    @commands.command(name='coolbot')
    async def cool_bot(self, ctx):
        """Is the bot cool?"""
        await ctx.send('This bot is cool. :)')

    @commands.command(name='top_role', aliases=['toprole'])
    @commands.guild_only()
    async def show_toprole(self, ctx, *, member: discord.Member=None):
        """Simple command which shows the members Top Role."""

        if member is None:
            member = ctx.author

        await ctx.send(f'The top role for {member.display_name} is {member.top_role.name}')
    
    @commands.command(name='perms', aliases=['perms_for', 'permissions'])
    @commands.guild_only()
    async def check_permissions(self, ctx, *, member: discord.Member=None):
        """A simple command which checks a members Guild Permissions.
        If member is not provided, the author will be checked."""

        if not member:
            member = ctx.author

        # Here we check if the value of each permission is True.
        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        # And to make it look nice, we wrap it in an Embed.
        embed = discord.Embed(title=f'Права для ```{member.name}```:', description=ctx.guild.name, colour=member.colour)
        try:
            embed.set_author(icon_url=member.avatar_url, name=str(member))
        except Exception:
            pass
        # \uFEFF is a Zero-Width Space, which basically allows us to have an empty field name.
        embed.add_field(name='\uFEFF', value=perms)

        await ctx.send(content=None, embed=embed)
        # Thanks to Gio for the Command.

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
async def setup(bot):
    await bot.add_cog(MembersCog(bot))