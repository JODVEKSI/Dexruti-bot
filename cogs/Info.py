import discord
from discord.ext import commands
import asyncio
import emo
import data
from discord import Emoji

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def serverinfo(self, ctx):
        emote = discord.Emoji
        server = ctx.guild
        b = await ctx.guild.bans()
        online = 0
        for s in server.members:
            if str(s.status) == 'online' or str(s.status) == 'idle' or str(s.status) == 'dnd':
                online += 1
        offline = 0
        for s in server.members:
            if str(s.status) == 'offline':
                offline += 1
        idle = 0
        for s in server.members:
            if str(s.status) == 'idle':
                idle += 1
        dnd = 0
        for s in server.members:
            if str(s.status) == 'dnd':
                dnd += 1       
        bots = [bot for bot in ctx.guild.members if bot.bot]   
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        categories = len(ctx.guild.categories)
        channels = text_channels + voice_channels
        embed = discord.Embed(title=f"{server.name}", color=data.color2)
        embed.add_field(name="About", value=f"**Name:** {server.name}\n**ID:** {server.id}\n**Owner:** {server.owner}({server.owner.mention})\n**Region:** {str(server.region).capitalize()}\n**Verficiation Level:** {str(server.verification_level).capitalize()}\n**Created At:** {server.created_at.__format__('%A, %d. %B %Y')}\n**Admin Perms:** {len([role for role in ctx.guild.roles if role.permissions.administrator])}", inline=False)
        embed.add_field(name="Members", value=f"**Total:** {ctx.guild.member_count}\n**Online:** {online}\n**Offline:** {offline}\n**Do not disturb:** {dnd}\n**Idle:** {idle}\n**Bots:** {str(len(bots))}", inline=False)
        embed.add_field(name="Features", value='\n'.join(f'{emo.tick}: {x}' for x in ctx.guild.features), inline=False)
        embed.add_field(name="Channels", value=f"**Total:** {channels}\n**Text Channels:** {text_channels}\n**Voice Channels:** {voice_channels}\n**Categories:** {categories}", inline=False)
        if len(ctx.guild.roles) <= 20:
            embed.add_field(name=f"Server Roles [{len(server.roles)}]", value=", ".join([str(r.mention) for r in ctx.guild.roles]), inline=False)
        else: 
            embed.add_field(name=f"Server Roles [{len(server.roles)}]", value="Too many roles can't show them here.", inline=False)
        embed.set_thumbnail(url=ctx.guild.icon_url)  
        await ctx.send(embed=embed)

    @commands.command()
    async def members(self, ctx):
        server = ctx.guild
        online = 0
        for s in server.members:
            if str(s.status) == 'online' or str(s.status) == 'idle' or str(s.status) == 'dnd':
                online += 1
        idle = 0
        for s in server.members:
            if str(s.status) == 'idle':
                idle += 1
        dnd = 0
        for s in server.members:
            if str(s.status) == 'dnd':
                dnd += 1
        offline = 0
        for s in server.members:
            if str(s.status) == 'offline':
                offline += 1
        total = online + offline        
        embed = discord.Embed(title=f"{server.name}", description=f"**Total Members:** {total}\n{emo.on} **Online:** {online}\n{emo.dn} **Do Not Disturb:** {dnd}\n{emo.idl} **Idle:** {idle}\n{emo.of} **Offline:** {offline}", color=data.color2)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))
