from datetime import datetime
import schedule

def monthly_job(job, t=None):
    date = datetime.today().day
    if t is not None and date == 1:
        schedule.every().day.at(t).do(job)


def weekday_job(job, t=None):
    week = datetime.today().weekday()
    if t is not None and week < 5:  # 0 - monday to 6 - sunday
        schedule.every().day.at(t).do(job)


def friday_job(job, t=None):
    week = datetime.today().weekday()
    if t is not None and week == 5:  # 0 - monday to 6 - sunday
        schedule.every().day.at(t).do(job)


def daily_job(job, t=None):
    if t is not None:
        schedule.every().day.at(t).do(job)


def hourly_job(job):
    schedule.every().hour.do(job)
