import discord
from discord.ext import commands
from datetime import datetime
import en



link = "https://dsc.gg/dexruti-music"


class invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.launch_time = datetime.utcnow()


    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(title = "Dexruti", description = f"[Click Here To Invite Me]({link})", color = en.color)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(invite(bot))


