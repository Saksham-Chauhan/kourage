from discord.ext import commands
from helper.jobs import *
from process.quotes.main import *
import asyncio
import schedule

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print("Welcome to Kourage...")


def init_schedules():
    weekday_job(job_morning_quote, '11:00')
    weekday_job(job_evening_work_log, '19:00')
    weekday_job(job_friday_meeting, '16:00')


async def run_schedules():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)


# Main driver code
init_schedules()
client.loop.create_task(run_schedules())
client.run(os.environ.get('TOKEN'))
