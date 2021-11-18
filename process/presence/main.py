import discord
import datetime
from helper import logger, plotter
from helper.webhook import send_webhook
from process.presence.embeds import get_graph_embed

data = dict()  # GLOBAL DATA
logger = logger.Logger("kourage-presence")


async def load_members(guild):
    result = dict()
    for member in guild.members:
        for role in member.roles:
            if role.name == "Koders":
                if member.status == discord.Status.online:
                    result[member.name] = {"total_time": datetime.timedelta(0), 'start_time': datetime.datetime.now()}
                else:
                    result[member.name] = {'total_time': datetime.timedelta(0), 'start_time': datetime.timedelta(0)}
    return result


async def reset_timer():
    global data
    data = dict()


async def update_timer(member, status):
    if member in data.keys():
        if status == 'online':
            data[member]['start_time'] = datetime.datetime.now()
        else:
            data[member]['total_time'] += (datetime.datetime.now() - data[member]['start_time'])
            data[member]['start_time'] = datetime.timedelta(0)


async def daily_presence_job(guild):
    global data
    plotter.plot_graph(data)
    webhook_url = ""
    send_webhook(webhook_url, get_graph_embed)
    data = load_members(guild)
    await reset_timer()
