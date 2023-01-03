import discord
from discord.ext import commands
from discord.utils import get
import json

with open('config.json', 'r') as f:
    config = json.load(f)

print(config)

bot = commands.Bot(command_prefix="*", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('---> Bot Online')

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! `{round(ctx.bot.latency * 1000)}ms`")

@bot.event
async def on_voice_state_update(member, before, after):
    try:
        if after.channel != None:
            if after.channel.id == config["channel"]:
                for guild in bot.guilds:
                    maincategory = discord.utils.get(
                        guild.categories, id = config["category"])
                    new_channel = await guild.create_voice_channel(name=f'{member.display_name}\'s VC',user_limit="2" , category=maincategory)
                    await new_channel.set_permissions(member, connect=True, manage_channels=True, mute_members=True)
                    await member.move_to(new_channel)

                    def check(x, y, z):
                        return len(new_channel.members) == 0
                    await bot.wait_for('voice_state_update', check=check)
                    await new_channel.delete()
    except:
        return
bot.run(config["token"])