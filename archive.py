import os
import time
import glob
import discord
import requests
import subprocess
from discord.utils import get
from discord.ext import commands
from discord.ext.tasks import loop
import io
import sys
from io import StringIO

import embeds

async def _archive(id, admin_channel, bot, logger, singleChannel, discord_key):
    #while True:
    if not id:
        raise Exception("ID not defined")

    fptr = open(r'stream/dce_stdin', 'w+')
    data = ('guild: ', 'channel: ') [singleChannel] + str(id) + '\n' + 'token: ' + os.environ.get('DISCORD_KEY')
    fptr.writelines(data)
    fptr.close()
    while not os.path.exists('stream/o_stdin'):
        time.sleep(1)

    os.remove('stream/o_stdin')

    files = glob.glob('stream/files/*')

    for file in files:
        await admin_channel.send(file = discord.File(file))

    fptr = open(r'stream/dce_stdin', 'w+')
    fptr.write('done')
    fptr.close()
    time.sleep(3)
    
async def __delete(ctx, logger):
    logger.info("~__delete called for " + str(ctx.channel.id))
    try:
        await ctx.channel.delete();
    except Exception as _err:
        raise Exception("Failed deleting channel " + str(ctx.channel.id) + " " + ctx.channel.name + "\nError:-\n" + _err)
