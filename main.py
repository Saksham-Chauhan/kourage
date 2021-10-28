from discord.ext import commands
from helper.jobs import *
import asyncio
import schedule

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print("Bot is ready.")


weekday_job(job_morning_quote(), '11:00')
weekday_job(job_evening_work_log(), '19:00')
weekday_job(job_friday_meeting(), '16:00')

while True:
    schedule.run_pending()
    asyncio.sleep(60)

client.run(os.environ.get('TOKEN'))
