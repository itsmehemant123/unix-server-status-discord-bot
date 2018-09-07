import discord
import json
import logging
import inspect
from discord.ext import commands
from serverstats import ServerStats

logging.basicConfig(level=logging.INFO)

with open('./config/auth.json') as data_file:
    auth = json.load(data_file)

initial_extensions = ['serverstats']
bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'), description='Server Status bot.')

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            logging.error(f'Failed to load extension {extension}.')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='Server Status', type=0, url='https://github.com/itsmehemant123/unix-server-status-discord-bot'))
    logging.info('Logged in as:{0} (ID: {0.id})'.format(bot.user))

bot.run(auth['token'])
