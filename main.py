from discord.ext import commands
from helper.jobs import *
from process.quotes.main import *
from process.presence.main import update_timer, daily_presence_job
from helper.logger import Logger
from dotenv import load_dotenv, find_dotenv
import asyncio
import schedule

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)

# TODO -> Hourly -> Tech meme
# TODO -> Daily -> Presence, Sentiments, Opened tickets, Spent time
# TODO -> Weekdays -> Attendance -> Morning, Post lunch, Quotes
# TODO -> Friday -> Meeting reminder, Chart spent time
# TODO -> Monthly -> Finances -> In/Out (Difference) + Graph, Team -> In/Out (Difference) + Graphs,
#  Issues (Opened/Closed) + Gantt chart

logger = Logger('kourage')


@client.event
async def on_ready():
    print("Welcome to Kourage...")


@client.event
async def on_member_update(usr_before, usr_after):
    logger.info('Status: ' + usr_before.name + '/' + str(usr_before.status))  # logging only for removing project errors
    logger.info('Status: ' + usr_after.name + '/' + str(usr_after.status))
    await update_timer(usr_after.name, usr_after.status)


def init_schedules():
    weekday_job(job_morning_quote, '11:00')
    weekday_job(job_evening_work_log, '19:00')
    friday_job(job_friday_meeting, '16:00')
    daily_job(daily_presence_job, '21:00')


async def run_schedules():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)


# Main driver
load_dotenv(find_dotenv())
init_schedules()
client.loop.create_task(run_schedules())
client.run(os.environ.get('TOKEN'))
