import discord 
from discord.ext import commands
import time



class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Get the bot's current websocket and API latency."""
        start_time = time.time()
        message = await ctx.send("Testing Ping...")
        end_time = time.time()


        await message.edit(content=f"Pong! {round(self.bot.latency * 1000)}ms")


def setup(bot):
    bot.add_cog(ping(bot))