import os
import urllib.request
import json
import io
import aiohttp
import discord
from dotenv import load_dotenv
from discord.ext import commands

# Get token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up bot interaction
bot = commands.Bot(command_prefix='$xkcd ')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# Functions


@bot.command()
async def comic(ctx, arg=''):
    # load json with given arg, if empty it will load current comic
    if arg == '':
        with urllib.request.urlopen(f'https://xkcd.com/info.0.json') as url:
            json_data = json.loads(url.read().decode())
    else:
        comic_number = int(arg)
        with urllib.request.urlopen(f'https://xkcd.com/{comic_number}/info.0.json') as url:
            json_data = json.loads(url.read().decode())

    # send http req and upload image to discord
    async with aiohttp.ClientSession() as sesh:
        async with sesh.get(json_data['img']) as resp:
            if resp.status != 200:
                return await ctx.send('Could not download file...')
            img = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(img, f'xkcd_{json_data["num"]}.png'))


# Run bot
bot.run(TOKEN)
