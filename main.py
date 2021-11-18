import discord
from discord.ext import commands
import time
import traceback
import discord
import asyncio
import psutil
from psutil import *
from datetime import datetime as dt
from discord.ext.commands.bot import when_mentioned
from discord.ext.commands.help import HelpCommand
import youtube_dl
import calendar
import datetime
import os
from platform import python_version
import data
intents = discord.Intents(members=True)
client=discord.Client(intents=intents)
intents = discord.Intents.all()
client = commands.Bot(command_prefix= '+', intents=intents, help_command=None)
startTime = int(time.time())

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Activity(
    type=discord.ActivityType.listening, name=f'@Dexruti'))
  print(f"[+] READY")






@client.event
async def on_guild_join(guild):
    
    user = client.get_user(int(583541611833851904))
    channel = guild.text_channels[0]
    invite = await channel.create_invite(unique=True)
    embed = discord.Embed(title="Dexruti", color=0x72FFF2, description=f"Joined A New Server!")
    embed.add_field(name='Server Name', value=f'**{guild.name}**', inline=False)
    embed.add_field(name='Server Owner', value=f'**{guild.owner}**', inline=False)
    embed.add_field(name="Total Members", value=f"**{len(guild.members)}**", inline=False)
    embed.add_field(name="Invite Link", value=invite, inline=False)
    embed.add_field(name="Now We Are In", value=f"{len(client.guilds)} Servers")
    embed.set_thumbnail(url=guild.icon_url)
    
    await user.send(embed=embed)


@client.command()
async def userinfo(ctx, *, user: discord.Member = None): # b'\xfc'
    if user is None:
        user = ctx.author      
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=0xdfa3ff, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Join position", value=str(members.index(user)+1))
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='ID: ' + str(user.id))
    return await ctx.send(embed=embed)



def get_years(timeBetween, year, reverse):
    years = 0

    while True:
        if reverse:
            year -= 1
        else:
            year += 1

        year_days = 366 if calendar.isleap(year) else 365
        year_seconds = year_days * 86400

        if timeBetween < year_seconds:
            break

        years += 1
        timeBetween -= year_seconds

    return timeBetween, years, year

def get_months(timeBetween, year, month, reverse):
    months = 0

    while True:
        month_days = calendar.monthrange(year, month)[1]
        month_seconds = month_days * 86400

        if timeBetween < month_seconds:
            break

        months += 1
        timeBetween -= month_seconds

        if reverse:
            if month > 1:
                month -= 1
            else:
                month = 12
                year -= 1
        else:
            if month < 12:
                month += 1
            else:
                month = 1
                year += 1

    return timeBetween, months

def getReadableTimeBetween(first, last, reverse=False):
    timeBetween = int(last-first)
    now = dt.now()
    year = now.year
    month = now.month

    timeBetween, years, year = get_years(timeBetween, year, reverse)
    timeBetween, months = get_months(timeBetween, year, month, reverse)

    weeks   = int(timeBetween/604800)
    days    = int((timeBetween-(weeks*604800))/86400)
    hours   = int((timeBetween-(days*86400 + weeks*604800))/3600)
    minutes = int((timeBetween-(hours*3600 + days*86400 + weeks*604800))/60)
    seconds = int(timeBetween-(minutes*60 + hours*3600 + days*86400 + weeks*604800))
    msg = ""

    if years > 0:
        msg += "1 year, " if years == 1 else "{:,} years, ".format(years)
    if months > 0:
        msg += "1 month, " if months == 1 else "{:,} months, ".format(months)
    if weeks > 0:
        msg += "1 week, " if weeks == 1 else "{:,} weeks, ".format(weeks)
    if days > 0:
        msg += "1 day, " if days == 1 else "{:,} days, ".format(days)
    if hours > 0:
        msg += "1 hour, " if hours == 1 else "{:,} hours, ".format(hours)
    if minutes > 0:
        msg += "1 minute, " if minutes == 1 else "{:,} minutes, ".format(minutes)
    if seconds > 0:
        msg += "1 second, " if seconds == 1 else "{:,} seconds, ".format(seconds)

    if msg == "":
        return "0 seconds"
    else:
        return msg[:-2]


@client.command()
async def botinfo(ctx):
    total_members = [x.id for x in client.get_all_members()]
    total_channels = [x.id for x in client.get_all_channels()]
    text_channel_list = []
    for guild in client.guilds:
      for channel in guild.text_channels:
       text_channel_list.append(channel)
    voice_channel_list = []
    for guild in client.guilds:
     for channel in guild.voice_channels:
      voice_channel_list.append(channel)
    proc = Process()
    cpuThred = os.cpu_count()
    cpu_usage = psutil.cpu_percent(interval=1)
    memStats = psutil.virtual_memory()
    memPerc = memStats.percent
    memUsed = memStats.used
    memTotal = memStats.total
    memUsedGB = "{0:.1f}".format(((memUsed / 1024) / 1024) / 1024)
    memTotalGB = "{0:.1f}".format(((memTotal/1024)/1024)/1024)
    mem_total = virtual_memory().total / (1024**2)
    mem_of_total = proc.memory_percent()
    mem_usage = mem_total * (mem_of_total / 100)
    currentTime = int(time.time())
    timeString  = getReadableTimeBetween(startTime, currentTime)
    embed = discord.Embed(description=f'{data.name}', color=data.color2, inline=False)
    embed.set_author(name="Bot Name")
    embed.add_field(name="Cpu Stats", value=f"Usage - {cpu_usage}%\nThreads - {cpuThred}", inline=False)
    embed.add_field(name="Servers", value=f"{len(client.guilds)}", inline=False)
    embed.add_field(name="Members", value=f"{len(total_members)} Total", inline=False)
    embed.add_field(name="Channels", value=f"{len(total_channels)} Total\n{len(text_channel_list)} Text\n{len(voice_channel_list)} Voice", inline=False)
    embed.add_field(name="Memory Stats", value=f"Total Memory - {memTotalGB} GB\nPercent - {memPerc}%\nUsed - {memUsedGB} GB\nUsage - {mem_usage:,.3f} / {mem_total:,.0f} GB ({mem_of_total:.0f}%)", inline=False)
    embed.add_field(name="Ping", value=f"Websocket - {int(client.latency * 1000)}ms", inline=False)
    embed.add_field(name="Uptime", value=f"{timeString}", inline=False)
    embed.add_field(name="Developers", value=f"{data.developers}", inline=False)
    embed.add_field(name="Language", value=f"Python {python_version()}", inline=False)
    embed.set_footer(text=f"Made with discord.py {python_version()}", icon_url="https://images-ext-1.discordapp.net/external/0KeQjRAKFJfVMXhBKPc4RBRNxlQSiieQtbSxuPuyfJg/http/i.imgur.com/5BFecvA.png")
    await ctx.send(embed=embed)


@client.command(name="help", description="shows all commands")
async def help(ctx):
  embed = discord.Embed(title= "**Dexruti Help Dialog**", 
  description=f"• Prefix for this server is `+`\n • Total commands: 22 | Usable by you: 22 \n • Type `+help <command | module>` for more info. ", 
  color=discord.Color.blue()) 
  embed.add_field(name='**Music**', value='`connect`, `play`, `disconnect`, `pause`, `next`, `stop`, `previous`, `shuffle`, `repeat`, `queue`, `volume`, `up`, `down`, `lyrics`, `eq`, `adveq`, `playing`, `skipto`, `restart`, `seek` ', inline=False)
  embed.add_field(name='**Ping**', value='`ping`', inline=False)
  embed.add_field(name='**Invite**', value='`invite`', inline=False)

  await ctx.send(embed=embed)



extensions = ['cogs.invite', 'cogs.ping', 'cogs.Music']
if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
            print(f"LOADED: {extension}")
        except Exception as e:
            print(f"Error loading: {extension}")
            traceback.print_exc()

client.run("(TOKEN)")  
