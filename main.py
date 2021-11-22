from discord.ext import commands
from discord.ext.commands import CommandNotFound

from helper.jobs import *
from process.quotes.main import *
from process.presence.main import update_presence_timer, daily_presence_job
from process.sentiment.main import daily_sentiment_job
from process.spent_time.main import daily_spent_job
from process.subreddit.main import reddit_tech_meme
from helper.logger import Logger
from dotenv import load_dotenv, find_dotenv
import asyncio
import schedule

intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)

# TODO -> Weekdays -> Attendance -> Morning, Post lunch, Quotes
# TODO -> Monthly -> Finances -> In/Out (Difference) + Graph, Team -> In/Out (Difference) + Graphs,
#  Issues (Opened/Closed) + Gantt chart

logger = Logger()


@client.event
async def on_ready():
    print("Welcome to Kourage...")


@client.event
async def on_member_update(usr_before, usr_after):
    logger.info('Status: ' + usr_before.name + '/' + str(usr_before.status))  # logging only for removing project errors
    logger.info('Status: ' + usr_after.name + '/' + str(usr_after.status))
    await update_presence_timer(usr_after.name, usr_after.status)


def init_schedules():
    weekday_job(job_morning_quote, '11:00')
    weekday_job(job_evening_work_log, '19:00')
    friday_job(job_friday_meeting, '16:00')
    daily_job(daily_presence_job, '21:00')
    daily_job(daily_sentiment_job, '21:10')
    daily_job(daily_spent_job(), '23:30')
    friday_job(daily_spent_job(), '18:00')
    hourly_job(reddit_tech_meme())



async def run_schedules():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)


# Main driver
if __name__ == "__main__":
    try:
        load_dotenv(find_dotenv())
        init_schedules()
        client.loop.create_task(run_schedules())
        client.run(os.environ.get('TOKEN'))
    except CommandNotFound:
        pass  # For handling command not found errors
    except Exception as _e:
        logger.warning("Exception found at main worker. Reason: " + str(_e), exc_info=True)
