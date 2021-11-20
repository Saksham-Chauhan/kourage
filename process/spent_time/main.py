from redminelib.exceptions import ResourceAttrError
from datetime import datetime
from helper.logger import Logger
from helper.plotter import plot_spent_graph
from helper.webhook import send_webhook
from helper.redmine import RedmineConfigKey
from process.spent_time.embed import get_sentiment_graph_embed
from dotenv import load_dotenv, find_dotenv
import os


logger = Logger()
load_dotenv(find_dotenv())


async def spent_time():
    redmine = RedmineConfigKey().initialize()

    today = datetime.now()
    time_entries = redmine.time_entry.filter(from_date=today)

    data, message = dict(), str()
    for entry in time_entries:

        if entry['user']['name'] not in data.keys():  # For plotting the graph
            data[entry['user']['name']] = entry['hours']
        elif entry['user']['name'] in data.keys():
            data[entry['user']['name']] += float(entry['hours'])

        try:  # For making the message
            message += (str(entry["user"]["name"]) + " " + "(Issue#" + str(entry["issue"]["id"]) + ")" + ' - ' + str(float(entry['hours'])) + ' hour(s)')
        except ResourceAttrError:
            message += (str(entry["user"]["name"]) + ' - ' + str(float(entry['hours'])) + ' hour(s)' + "** PLEASE "
                                                                                                       "ALLOCATE ")
        return data, message


async def daily_spent_job():
    data, message = await spent_time()
    plot_spent_graph(data)
    embed = get_sentiment_graph_embed(message)
    webhook_url = os.environ.get('SPENT_WEBHOOK_URL')
    send_webhook(webhook_url, embed)
