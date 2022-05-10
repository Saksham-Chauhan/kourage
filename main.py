import discord
import os
from discord.ext import commands

webhook_url=os.getenv('WEBHOOK')
token=os.getenv('TOKEN')
monitor_channel_id=os.getenv('CHANNELID')

bot = commands.Bot(command_prefix='!')

def send_webhook(url, content):
    import requests #dependency
    data = {
        "content" : content,
    }

    result = requests.post(url, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))

@bot.event
async def on_ready():
    print("Logged in as" + bot.user)

@bot.event
async def on_message(message):
    if int(message.channel.id) == int(monitor_channel_id):
        send_webhook(webhook_url, message.content)

bot.run(token)

