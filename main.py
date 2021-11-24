from email.message import EmailMessage
import random
import smtplib, ssl 
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
import os
import discord
import platform
import asyncio
from uuid import uuid4
from colorama import init
from termcolor import colored
from discord.ext.commands import bot
from discord.ext import commands
import time
import logging
import datetime

machine = platform.node()
init()

logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)

class Logger:
    def __init__(self, app):
        self.app = app

    def info(self, message):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', 'yellow'))

    def success(self, message):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', 'green'))

    def error(self, message):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', 'red'))

    def color(self, message, color):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', color))

logger = Logger("kourage-emails")
bot = commands.Bot(command_prefix="~")
sender_email = None
sender_passwd = None

@bot.event
async def on_command_error(ctx, error):
#################################
# FIXME: JSON File input
##################################
import sys
import subprocess
import sqlite3
import requests
import os
import json
import glob
import discord
import datetime

import asyncio
from uuid import uuid4
from sqlite3.dbapi2 import Cursor
from discord.ext.tasks import loop
from discord.ext.commands.errors import CommandNotFound
from discord.utils import get
from discord.ext import commands

import embeds
import sqlite_cmds as SQLITE

#################################################
#                   GLOBALS                     #
#################################################
#                                               #
intents = discord.Intents.all()                 #
bot = commands.Bot(command_prefix="~",          #
        intents = intents)                      #
logger = embeds.Logger("kourage-profile")       #
embeds.logger = logger                          #
                                                #
message_id = 874543919357124668                 #
ticket_channel_id = 870538319807803422          #
ticket_channel = None                           #
#################################################
#       LIST FOR MAINTAINING ORDER              #
#################################################
kontent_file = open('kontent_sheet.json')       #
kontent_json = json.load(kontent_file)          #
                                                #
base_list = kontent_json['base_list']           #
base_dict = kontent_json['base_dict']           #
role_list = kontent_json['role_list']           #
role_dict = kontent_json['role_dict']           #
#################################################

def environ_check(var):
    if not var in os.environ:
        raise Exception("'" + var + "' not found in the environ list.")

@bot.event
async def on_ready():
    global ticket_channel
    try:
        ticket_channel = bot.get_channel(ticket_channel_id)
        logger.info('Tickets to be send on: ' + str(ticket_channel.id) + '/' + ticket_channel.name)
    except Exception as err:
        logger.error('~on_ready: ' + str(err))
        return

    db = sqlite3.connect('db/profile.sqlite')
    cursor = db.cursor()
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS MAIN(
            DISCORD_ID TEXT,
            NAME TEXT,
            PHONE INTEGER,
            MAIL TEXT,
            BIO TEXT,
            DOB TEXT,
            PROJECTS TEXT,
            WHATSAPP INTEGER,
            FACEBOOK TEXT,
            INSTAGRAM TEXT,
            REDMINE TEXT)
            ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS DEVELOPER(
            DISCORD_ID TEXT,
            FAV_LANG TEXT,
            GITHUB TEXT,
            FAV_TEXT_EDITOR TEXT,
            SKILLS TEXT)
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS MARKETING(
            DISCORD_ID TEXT,
            FAV_TOOLS TEXT,
            SKILLS TEXT,
            FAV_BRAND TEXT,
            HOBBIES TEXT
        )''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS DESIGNER(
            DISCORD_ID TEXT,
            FAV_TOOLS TEXT,
            PORTFOLIO TEXT,
            SKILLS TEXT
        )''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS KONTENT(
            DISCORD_ID TEXT,
            SKILLS TEXT,
            FAV_TOOLS TEXT,
            FAV_BLOGS TEXT,
            FAV_BOOKS TEXT
        )''')

    except Exception as err:
        logger.error('SQLite: ' + str(err))
        return

    logger.success("Kourage is running at version 0.1.0")

@bot.event
async def on_raw_reaction_add(ctx):
    user = ctx.member

    if user.bot is True or ctx.message_id != message_id:
        return

    channel = await bot.fetch_channel(ctx.channel_id)
    try:
        await user_profile(channel, user)
    except Exception as err:
        logger.error("'on_react': " + str(err))
        return
    logger.success("on_raw_reaction_add executed successfully.")
import datetime
import json
import os
# Logging format
import logging
import platform
import time
import sqlite3
import sys
import traceback
from sqlite3.dbapi2 import Cursor
from discord import channel, message
from discord.enums import MessageType
import embed as embed
from discord.utils import get
import discord
import requests
from colorama import init
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
import embed as EMBEDS
import embed

intents = discord.Intents.all()
logger = embed.Logger("kourage-attendance")


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='.', intents=intents)

# TODO -> Weekdays -> Attendance -> Morning, Post lunch, Quotes
# TODO -> Monthly -> Finances -> In/Out (Difference) + Graph, Team -> In/Out (Difference) + Graphs,
#  Issues (Opened/Closed) + Gantt chart

logger = Logger()


@client.event
async def on_ready():
    print("Welcome to Kourage...")


@bot.event
async def on_command_error(ctx, error):
    await ctx.message.delete()
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.send("*Private messages.* ", delete_after = 60)
    elif isinstance(error, commands.MissingAnyRole):
        await ctx.send("*~Not have enough permission.*", delete_after = 60)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("*Command is missing an argument:* ", delete_after = 60)
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send("*This command is currenlty disabled. Please try again later.* ", delete_after = 60)
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("*You do not have the permissions to do this.* ", delete_after = 60)
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("*This command is not listed in my dictionary.*", delete_after = 60)
    await ctx.message.delete()
    logger.error(error)

def environ_check(var):
    if not var in os.environ:
        raise Exception("'" + var + "' not found in the environ list.")

# Client : Welcome Message + First Meeting Fixation
@bot.command()
async def client_aboard(ctx, arg1, arg2, arg3, arg4, arg5):
    logger.info('~client_aboard called.')
    sender = sender_email
    # client email id
    receiver = arg2

    msg = EmailMessage()
    msg['Subject'] = 'Thank you for choosing Koders! We would like to fix a meeting with you.'
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        # client name
        name = arg1
        date = arg3
        time = arg4
        Link = arg5

    HTML_File=open('client/client_aboard.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("Client : Welcome Aboard email successfully sent!")

# Client : Initiation Message
@bot.command()
async def client_initiation(ctx, arg1, arg2):
    logger.info('~client_initiation called.')
    sender = sender_email
    # client email id
    receiver = arg2

    msg = EmailMessage()
    msg['Subject'] = 'Yay! Your project is under consideration.'
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        # client name
        name = arg1

    HTML_File=open('client/client_initiation_msg.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("Client : Initiation email successfully sent!")

# Client : Confirmation Message
@bot.command()
async def client_confirm(ctx, arg1, arg2, arg3, arg4):
    logger.info('~client_confirm called.')
    sender = sender_email
    # client email id
    receiver = arg2

    msg = EmailMessage()
    msg['Subject'] = 'Congrats! Stay tuned for the updates regarding your project.'
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        # client name
        name = arg1
        project_name = arg3
        project_id = arg4

    HTML_File=open('client/client_confirm.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("Confirmation email successfully sent!")

# Client : Onboarding Message/ Kommunity : Onbaording Message
@bot.command()
async def client_onboard(ctx, arg1, arg2):
    logger.info('~client_onboard called.')
    sender = sender_email
    # client email id
    receiver = arg2

    msg = EmailMessage()
    msg['Subject'] = 'Welcome Aboard! Please check out our kommunity guidelines.'
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        # client name
        name = arg1

    HTML_File=open('client/client_onboard.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("Client : Welcome Onboard email successfully sent!")

# Client : Decline Message
@bot.command()
async def client_decline(ctx, arg1, arg2):
    logger.info('~client_decline called.')
    sender = sender_email
    # client email id 
    receiver = arg2

    msg = EmailMessage()
    msg['Subject'] = 'Sorry! Our timeline is too tight.'
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        # client name
        name = arg1

    HTML_File=open('client/client_decline.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("Sorry email successfully sent!")

# Client : Delivery Message
@bot.command()
async def client_thanks(ctx, arg1, arg2, arg3):
    logger.info('~client_thanks called.')
    sender = sender_email
    receiver = arg2

    msg = EmailMessage()
    msg['Subject'] = 'Hurray! We have successfully completed the project.'
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        name = arg1
        project_name = arg3

    HTML_File=open('client/client_thank_you.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("Delivery email successfully sent!")

# Client : ENDNOTE
@bot.command()
async def client_endnote(ctx, arg1, arg2, arg3):
    logger.info('~client_endnote called.')
    sender = sender_email
    receiver = arg2

    msg = EmailMessage()
    msg['Subject'] = 'Your response matters to us the most.'
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        name = arg1
        feedback_link = arg3

    HTML_File=open('client/client_endnote.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("Endnote email successfully sent!")

# Koders : Welcome Message + First Meeting Fixation
@bot.command()
async def koders_aboard(ctx, arg1, arg2, arg3):
    logger.info('~koders_aboard called.')
    sender = sender_email
    # receiver email id
    receiver = arg2

    msg = EmailMessage()
    msg['Subject'] = 'Welcome aboard to Koders !'
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        name = arg1
        Link = arg3

    HTML_File=open('koders/koders_aboard.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("Koders : Welcome Aboard email successfully sent!")

# Koders : Shortlist - Interview
@bot.command()
async def koders_interview(ctx, arg1, arg2, arg7, arg3, arg4, arg5, arg6):
    logger.info('~koders_interview called.')
    sender = sender_email
    # reciever email id
    receiver = arg2

    msg = EmailMessage()
    msg['Subject'] = 'You have been shortlisted! Here is the interview Invite.'
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        name = arg1
        position = arg7
        minutes = arg3
        date = arg4
        time = arg5
        Link = arg6

    HTML_File=open('koders/koders_interview.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("Koders : Interview email successfully sent!")

# Koders - GD Invite
@bot.command()
async def koders_gd(ctx, arg1, arg2, arg4, arg5, arg6):
    logger.info('~koders_gd called.')
    sender = sender_email
    # receiver email id
    receiver = arg2

    msg = EmailMessage()
    msg['Subject'] = 'GD Invite, Congrats for making it to the next round!'
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        # Koders name
        name = arg1
        date = arg4
        time = arg5
        Link = arg6

    HTML_File=open('koders/koders_gd.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("Koders : GD Invite email successfully sent!")

# Koders : Confirmation Message
@bot.command()
async def koders_confirm(ctx, arg3, arg1):
    logger.info('~koders_confirm called.')
    sender = sender_email
    receiver = arg1

    msg = EmailMessage()
    msg['Subject'] = 'Congratulations!! Koders is waiting for you.'
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        name = arg3

    HTML_File=open('koders/koders_confirm.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("Congratulations email successfully sent!")

# Koders : Onboarding Message
@bot.command()
async def koders_onboard(ctx, arg1, arg2):
    logger.info('~koders_onboard called.')
    sender = sender_email
    # Koders email id
    receiver = arg2

    msg = EmailMessage()
    msg['Subject'] = 'Welcome Aboard! Please check out our kommunity guidelines.'
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        name = arg1

    HTML_File=open('koders/koders_onboard.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("Koders : Welcome Onboard email successfully sent!")

# Koders : Decline Message
async def koders_decline(ctx, arg1, arg2, arg3):
    logger.info('~koders_decline called.')
    sender = sender_email
    receiver = arg2

    msg = EmailMessage()
    msg['Subject'] = 'Hi! Sorry'
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        name = arg1
        role = arg3

    HTML_File=open('koders/koders_decline.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("Sorry email successfully sent!")

# Koders : Tenure Review
@bot.command()
async def koders_tenure(ctx, arg1, arg2, arg6, arg3, arg4, arg5):
    logger.info('~koders_tenure called.')
    sender = sender_email
    # recepitent email id
    receiver = arg2

    msg = EmailMessage()
    msg['Subject'] = 'Tenure Review with Koders.'
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        # recepitent name
        name = arg1
        domain = arg6
        date = arg3
        time = arg4
        Link = arg5

    HTML_File=open('koders/koders_tenure.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("Tenure review email successfully sent!")

# Koders : ENDNOTE/ Kommunity EndNote Message
@bot.command()
async def koders_endnote(ctx, arg1, arg2, arg3, arg4):
    logger.info('~koders_endnote called.')
    sender = sender_email
    receiver = arg2

    msg = EmailMessage()
    msg['Subject'] = 'With best wishes, thank you and hoping to Kross paths again.'
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        name = arg1
        domain_work = arg3
        feedback_link = arg4

    HTML_File=open('koders/koders_endnote.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("Endnote email successfully sent!")

# Kommunity : Welcome + Initiation Message 
@bot.command()
async def kommunity_aboard(ctx, arg1, arg2):
    logger.info('~kommunity_aboard called.')
    sender = sender_email
    # Koders email id
    receiver = arg2

    msg = EmailMessage()
    msg['Subject'] = 'Welcome to Koders! Be a part of our amazing family.'
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        # Koders name
        name = arg1

    HTML_File=open('kommunity/kommunity_aboard.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("Kommunity : Welcome email successfully sent!")

# Kommunity : Opportunity Message
@bot.command()
async def kommunity_opportunity(ctx, arg1, arg2, arg3, arg4, arg5):
    logger.info('~kommunity_opportunity called.')
    sender = sender_email
    # receiver email id
    receiver = arg2

    msg = EmailMessage()
    msg['Subject'] = 'A good opportunity is waiting for you! '
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        # receiver name
        name = arg1
        date = arg3
        time = arg4
        Link = arg5

    HTML_File=open('kommunity/kommunity_opportunity.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("Kommunity : Opportunity email successfully sent!")

# For ALL : Termination Message
@bot.command()
async def terminate(ctx, arg1, arg2):
    logger.info('~terminate called.')
    sender = sender_email
    receiver = arg2

    msg = EmailMessage()
    msg['Subject'] = 'Termination from Koders.'
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        name = arg1

    HTML_File=open('all//terminate.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("For All : Termination email successfully sent!")

# For ALL : Alumini Message
@bot.command()
async def alumini(ctx, arg1, arg2):
    logger.info('~alumini called.')
    sender = sender_email
    receiver = arg2

    msg = EmailMessage()
    msg['Subject'] = 'A Bond Forever. Alumni World of Koders'
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        name = arg1

    HTML_File=open('all/alumini.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("For All : Alumini email successfully sent!")

# For ALL : Accept Resignation
@bot.command()
async def accept_resign(ctx, arg1, arg2):
    logger.info('~accept_resign called.')
    sender = sender_email
    receiver = arg2

    msg = EmailMessage()
    msg['Subject'] = 'Resignation Acceptance'
    msg['From'] = sender
    msg['To'] = receiver
    
    class Main:
        name = arg1

    HTML_File=open('all/accept_resign.html','r',encoding="utf-8")
    s = HTML_File.read().format(p=Main)
    msg.set_content(s, subtype='html')
    HTML_File.close()

    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender_email, password = sender_passwd)
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    await ctx.message.delete()
    logger.info("For All : Accept resignation email successfully sent!")

@bot.event
async def on_ready():
    global sender_email
    global sender_passwd
    try:
        environ_check('SENDER_EMAIL')
        environ_check('SENDER_PASSWD')

        sender_email = os.environ.get('SENDER_EMAIL')
        sender_passwd = os.environ.get('SENDER_PASSWD')
    except Exception as err:
        logger.error('~on_ready: ' + str(err))
        exit()
    logger.success('Kourage is running at version 0.1.0')
    logger.error(error)
@client.event
async def on_member_update(usr_before, usr_after):
    logger.info('Status: ' + usr_before.name + '/' + str(usr_before.status))  # logging only for removing project errors
    logger.info('Status: ' + usr_after.name + '/' + str(usr_after.status))
    await update_presence_timer(usr_after.name, usr_after.status)


# TODO
# Validation for Redmine API Key ------
async def user_profile(ctx, user):
    logger.info('~user_profile called.')
    welcome_embed = None
    try:
        conn  = sqlite3.connect('db/profile.sqlite')
        cur = conn.cursor()
        exec(SQLITE.sqlite_exist_in_table('cur', 'MAIN', 'DISCORD_ID', 'user.id'))
        if cur.fetchone()[0]:
            await embeds.error_title_embed(ctx, 'User ' + user.name + ' already exists!', 'Please update rather than creating your profile.')
            logger.error('Can not create a new profile. User ' + str(user.id) + '/' + user.name + ' exists in DB.')
            return

        welcome_embed = await embeds.initialize_embed(ctx, user)
        data = list()
        data_dict = dict()
        data_embed_dict = dict()
        idx = 0
        list_idx = 0

        for _keydict in base_dict:
            __key = [j for j in _keydict][0]

            data_dict['DISCORD_ID'] = "user.id"
            data_embed_dict['DISCORD_ID'] = "user.id"

            for i in base_list[__key]:
                __data = await embeds.desc_ctx_input(ctx, bot, i, _keydict[__key][i]['CONTENT'],
                        user = user, type = _keydict[__key][i]['TYPE'])
                data.append(__data)
                data_embed_dict[i] = __data
                data_dict[i] = "data[" + str(list_idx) + "]"
                list_idx+=1
            idx += 1
            exec(SQLITE.create_sqlite_cmd('cur', __key, data_dict))

        role_sqlite_dict = dict()
        idx = 0
        for _keydict in role_dict:
            __key = [j for j in _keydict][0]

            # In case the user doesn't have that role.
            if not __key in [i.name.upper() for i in user.roles]:
                continue

            role_embed_dict = dict()
            role_embed_dict[__key] = dict()
            role_embed_dict[__key]['DISCORD_ID'] = str(user.id)

            _role_sqlite_dict = dict()
            _role_sqlite_dict['DISCORD_ID'] = 'user.id'

            for i in role_list[__key]:
                __data = await embeds.desc_ctx_input(ctx, bot, i, _keydict[__key][i]['CONTENT'],
                        user = user, type = _keydict[__key][i]['TYPE'])
                data.append(__data)

                _role_sqlite_dict[i] = "data[" + str(list_idx) + "]"
                role_embed_dict[i] = __data
                list_idx += 1

            idx += 1
            role_sqlite_dict[__key] = _role_sqlite_dict

        for i in role_sqlite_dict:
            exec(SQLITE.create_sqlite_cmd('cur', i, role_sqlite_dict[i]))
        conn.commit()

        await __profile(ticket_channel, user, None, True)
        await welcome_embed.delete()

        await user.add_roles(discord.utils.get(ctx.guild.roles, name = 'Koders'))
    except Exception as err:
        await welcome_embed.delete()
        logger.error('~user_profile: ' + str(err))
        return

    await embeds.send_success_embed(ctx, 'Profile created successfully.', '')
    logger.success('~user_profile executed successfully.')

async def print_profile(ctx, user_id, _dict, cur, timeout = 60, isTextChannel = False):
    logger.info('print_profile called.')

    table_name, cmd = (SQLITE.sqlite_fetch_cmd('cur', _dict, 'DISCORD_ID', user_id))

    exec(cmd)
    row = cur.fetchone()
    j = 0
    send_dict = dict()
    for i in _dict[table_name]:
        if i.lower() == 'redmine':
            continue
        send_dict[i] = row[j]
        j+=1
    user = await bot.fetch_user(user_id)
    channel = ctx if isTextChannel else ctx.channel
    await embeds.send_inline(channel, user.name + ' ' + table_name, '', send_dict, timeout = timeout)

    logger.success('~print_profile executed successfully.')

async def __profile(ctx, user, timeout = 60, isTextChannel = False):
    logger.info('__profile called.')
    conn = sqlite3.connect('db/profile.sqlite')
    cur = conn.cursor()

    user_id = str(user.id)
    global base_list
    global role_list

    try:
        exec(SQLITE.sqlite_exist_in_table('cur', 'MAIN', 'DISCORD_ID', 'user_id'))
        if not cur.fetchone()[0]:
            await embeds.error_title_embed(ctx, '', str(user.mention) + ' not found', timeout = 5)
            return

        roles = list()
        for role in role_list:
            exec(SQLITE.sqlite_exist_in_table('cur', role, 'DISCORD_ID', 'user_id'))
            if cur.fetchone()[0]:
                roles.append({role: role_list[role]})

        await print_profile(ctx, user_id, {'MAIN': base_list['MAIN']}, cur, timeout, isTextChannel)
        for i in roles:
            await print_profile(ctx, user_id, i, cur, timeout, isTextChannel)
    except Exception as err:
        logger.error('SQLite: ' + str(err))
        return
def init_schedules():
    weekday_job(job_morning_quote, '11:00')
    weekday_job(job_evening_work_log, '19:00')
    friday_job(job_friday_meeting, '16:00')
    daily_job(daily_presence_job, '21:00')
    daily_job(daily_sentiment_job, '21:10')
    daily_job(daily_spent_job(), '23:30')
    friday_job(daily_spent_job(), '18:00')
    hourly_job(reddit_tech_meme())

# FOR PRODUCTION
bot = commands.Bot(command_prefix="~", intents=intents)

# TODO
# Remove sumyak1 and test.py

async def member_loader():
    member_list = []
    guild = bot.get_guild(534406455709663233) # Koders's guild id 534406455709663233
    role = discord.utils.get(guild.roles, name="Koders")
    for member in guild.members:
        if role in member.roles:
            member_list.append(member.id)
    return member_list

@bot.event
async def on_ready():  # triggers when bot is ready
    db = sqlite3.connect('db/ATTENDANCE.sqlite')
    cursor = db.cursor()
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Attendance_table(
            DATE TEXT,
            SHIFT TEXT,
            PRESENTEES TEXT,
            ABSENTEES TEXT
            )
        ''')
        db.commit()
        logger.warning("checking integrity of attendance db")

    except Exception as err:
        logger.error("exception caught at creating attendance db action: " + err.__class__ + " " + str(err))
        return

@bot.event
async def on_command_error(ctx, error):
    ctx.message.delete()
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.send("*Private messages.* ", delete_after=60)
    elif isinstance(error, commands.MissingAnyRole):
        await ctx.send("*~Not have enough permission.*", delete_after=60)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("*Command is missing an argument:* ", delete_after=60)
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send("*This command is currenlty disabled. Please try again later.* ", delete_after=60)
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("*You do not have the permissions to do this.* ", delete_after=60)
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("*This command is not listed in my dictionary.*", delete_after=60)
    logger.error(error)

# helper functions
def check(reaction, user):
    return str(reaction.emoji) == '⬆️' and user.bot is not True
async def take_reaction(msg, shift_status, timeout=1200.0, presentees=[]):
    shift_status=shift_status
    start = time.time()
    try:
        result = await bot.wait_for('reaction_add', check=check, timeout=timeout)
    except asyncio.TimeoutError:
        await msg.delete()

        # TODO
        # CTX for absent showing on attendance channel
        ctx = bot.get_channel(int(os.environ.get("CHANNEL_ID"))) # Channel id goes here
        logger.info(ctx)
        # Database entry
        today=datetime.date.today()
        date=str(today.strftime("%Y-%m-%d"))
        presentees = set(presentees)
        if not presentees:
            presentees.add("No Presentees.")
        members = set(await member_loader())
        absentees = members - presentees

        conn = sqlite3.connect('db/ATTENDANCE.sqlite')
        cur = conn.cursor()
        try:
            cur.execute('''INSERT INTO Attendance_table(DATE, SHIFT, PRESENTEES, ABSENTEES) VALUES (?, ?, ?, ?)''', (date,shift_status,str(presentees).replace("'",""),str(absentees).replace("'","")))
            conn.commit()
            logger.warning("Attendance added to db. \nPresentees - " + str(presentees)  + "\nAbsentees - "+str(absentees))
            embed=await show_absentees(date, shift_status, absentees)
            await ctx.send(embed=embed, delete_after=120)
            logger.info("absentees shown")
        except Exception as err:
            logger.error(str(err.__class__) + " " + str(err))

    else:
        reaction, user = result
        channel = await user.create_dm()

        date_time = datetime.datetime.now()
        embed = EMBEDS.attendance_dm(date_time.strftime("%D"), date_time.strftime("%H:%M:%S"), date_time.strftime("%A"))
        await channel.send(embed=embed)

        end = time.time()
        timeout = timeout - (end - start)
        logger.info(str(user.id) + '/' + user.name + ' reacted to attendance.')

        presentees.append(user.id)
        await take_reaction(msg, shift_status=shift_status, timeout=timeout, presentees=presentees)

#@bot.command()
async def take_attendance(channel, start_time, end_time):
    logger.info("function take attendance called")
    if(type(start_time)==datetime.datetime):
        if start_time.hour>15:
            shift_status="E"
        elif start_time.hour<15:
            shift_status="M"
        start_time =str(start_time.strftime(r"%I:%M"))
        end_time = str(end_time.strftime(r"%I:%M"))
    logger.warning("sending attendance")
    _embed = embed.attendance(start_time,end_time)
    msg = await channel.send(embed=_embed)
    await msg.add_reaction(emoji="⬆️")
    #msg=bot.get_channel(msg.channel.id)


    if start_time == "11:00" and end_time == "11:20":
        shift_status="M"
    elif start_time == "15:00" and end_time == "15:20":
        shift_status="E"
    else:
        shift_status=shift_status

    try:
        await take_reaction(msg, shift_status)
    except Exception as err:
        logger.error("exception caught at taking attendance" + str(err))
        return
    logger.info("function take attendance executed successfully")

@bot.command()
@commands.has_any_role("Kore")
async def manual_fire(ctx):
    logger.info("function manual fire called by " + str(ctx.author.name))

    start_time = datetime.datetime.now()
    timestamp = datetime.datetime.now()
    end_time = timestamp + datetime.timedelta(minutes = 20)
    channel = bot.get_channel(ctx.channel.id)
    embed = await take_attendance(channel, start_time, end_time)

    logger.info("function manual fire executed successfully.")
    await ctx.message.delete()
async def show_absentees(date, shift_status, absentees):
    logger.info("function show_absentees called.")

    if shift_status == "M":
        message = "Morning"
    elif shift_status == "E":
        message = "Evening"

    #message=""
    absentee_list = ""
    for absentee in absentees:
        username = await bot.fetch_user(absentee)
        absentee_list += str(username)+"\n"

    _embed=embed.simple_embed(title="Absent Users on :"+str(date)+"\nShift: "+message,description="")
    _embed.add_field(name='Users list:', value=absentee_list+"\n\n\n", inline=False)
    logger.info("List of absentees has been sent to the channel")

    return _embed

@bot.command() #TODO: add kore properties
async def leaves(ctx, *args):
    logger.info('~leaves is called by: ' + str(ctx.author.id) + '/' + ctx.author.name)
    author_role = ctx.author.roles
    role = ''
    for i in author_role:
        if str(i)=="Kore":
            role=str(i)
            break;
        else:
            role="Koders"
    if str(role) != "Kore" and args:
        not_access_embed=discord.Embed(title="Sorry You dont have access to view others leaves!",description="",colour=0x11806a)
        await ctx.send(embed=not_access_embed,delete_after=60)
        logger.warning(str(ctx.author.id)+" dont have access")
        await ctx.message.delete()
    if check_opening_time.hour < 15:
        shift_status="M"
    elif check_opening_time.hour > 15:
        shift_status="E"

    opening_time=str(timestamp.strftime(r"%I:%M %p"))
    ending_time=str(delta.strftime(r"%I:%M %p"))
    embed = EMBEDS.attendance(opening_time, ending_time)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction(emoji="⬆️")
    try:
        await take_reaction(msg,shift_status)
    except Exception as err:
        logger.error("'manual_fire': " + err)
        return

    start_date, end_date = await embed.data_input(ctx,bot)

    # TODO - set index accordingly to roles only
    # TODO - koders needs to be changed to Kore

    if not args: #check all attendances
        users = []
        if str(role) == "Kore":
            users=await member_loader()
            await embed.leave_and_attendance(ctx, bot, start_date, end_date, users, 1)
    today=datetime.date.today()
    current_date = today.strftime("%Y-%m-%d")
    leave_Embed=embed.simple_embed(title="Absent Users on :"+str(current_date)+" morning",description="")

    try:
        cur.execute('''SELECT DISTINCT Users_DB_Attendance.User_ID FROM Users_DB_Attendance WHERE NOT EXISTS (SELECT Attendance_DB.User_ID FROM Attendance_DB WHERE Users_DB_Attendance.User_ID = Attendance_DB.User_ID AND Attendance_DB.Date = ?)''', [current_date])
    except Exception as err:
        logger.error(err.__class__ + " " + str(err))

        elif str(role) != "Kore":
            users.append(str(ctx.author.id))
            await embed.leave_and_attendance(ctx, bot, start_date, end_date, users, 1)
    else:
        users = []
        for arg in args:
            arg:discord.Member
            users.append(str(arg.strip("!@<>")))

        await embed.leave_and_attendance(ctx, bot, start_date, end_date, users, 1)
    await ctx.message.delete()
    morning_absent = cur.fetchall()
    morning_leave_list=""

    for i in morning_absent:
        user_id=str(i)
        bad_chars = ['(', ')', ',', "'"]
        for i in bad_chars:
            user_id=user_id.replace(i, '')

    logger.success('~__profile executed successfully.')
        username = await bot.fetch_user(user_id)
        morning_leave_list=morning_leave_list+str(username)+"\n"

@bot.command()
@commands.has_any_role("Koders")
async def profile(ctx, *, user_mentions):
    logger.info('~profile called.')
    try:
        await ctx.message.delete()
        welcome_embed = await embeds.initialize_embed(ctx, ctx.author)
        user_list = user_mentions.split()
        users = set()

        is_kore = 'kore' in [i.name.lower() for i in ctx.author.roles]
    leave_Embed.add_field(name='Users list:', value = morning_leave_list+"\n\n\n", inline=False)
    await ctx.send(embed = leave_Embed,delete_after=1200.0)
    logger.info("'absentees_morning' done successfully.")

#@bot.command()
async def absentees_evening(ctx):
    logger.info("'~absentees_evening' called successfully.")

    conn = sqlite3.connect('Attendance_DB.sqlite')
    cur = conn.cursor()

    today=datetime.date.today()
    current_date = today.strftime("%Y-%m-%d")
    leave_Embed=embed.simple_embed(title="Absent Users on :"+str(current_date)+" evening",description="")
    try:
        cur.execute('''SELECT DISTINCT Users_DB_Attendance.User_ID FROM Users_DB_Attendance WHERE NOT EXISTS (SELECT Attendance_DB.User_ID FROM Attendance_DB WHERE Users_DB_Attendance.User_ID = Attendance_DB.User_ID AND Attendance_DB.Date = ?)''', [current_date])
    except Exception as err:
        logger.error(err.__class__ + " " + str(err))

    morning_absent = cur.fetchall()
    morning_leave_list=""
    evening_leave_list=""
    for i in morning_absent:
        user_id=str(i)
        bad_chars = ['(', ')', ',', "'"]
        for i in bad_chars:
            user_id=user_id.replace(i, '')

        for user in user_list:
            users.add(await bot.fetch_user(int(user[3 : -1])))
        username = await bot.fetch_user(user_id)
        morning_leave_list=morning_leave_list+str(username)+"\n"

        for user in users:
            if user.id != ctx.author.id:
                if not is_kore:
                    await embeds.error_title_embed(ctx, "Unauthorized Access", 'Not authorized to access details of ' + user.mention + '!')
                    logger.error('Unauthorized Access by ' + ctx.author.name + ' for ' + str(user.id) + '/' + user.name + '.')
                    continue
            await __profile(ctx, user)

        await welcome_embed.delete()
    except Exception as err:
        await welcome_embed.delete()
        logger.error('~profile: ' + str(err))
        return

    logger.success('~profile executed successfully.')

async def _update(ctx, user, key):
    logger.info("'~_update' called.")

    conn = sqlite3.connect('db/profile.sqlite')
    cur = conn.cursor()
    key_in_base = key in base_list
    try:
        search_dict = base_dict if key_in_base else role_dict
        search_list = base_list if key_in_base else role_list
    leave_Embed.add_field(name='Users list absent in morning and evening both :', value = morning_leave_list+"\n\n\n", inline=False)

    #evening
    half_leave_list=[]
    try:
        cur.execute('''SELECT DISTINCT Users_DB_Attendance.User_ID FROM Users_DB_Attendance WHERE (SELECT Attendance_DB.User_ID   FROM Attendance_DB WHERE Users_DB_Attendance.User_ID=Attendance_DB.User_ID AND Attendance_DB.Date=? ) ''',[current_date])
    except Exception as err:
        logger.error(err.__class__ + " " + str(err))

    half_absent = cur.fetchall()

    for i in half_absent:
            user_id=str(i)
            bad_chars = ['(', ')', ',', "'"]
            for i in bad_chars:
                user_id=user_id.replace(i, '')

        data = list()
        data_dict = dict()
        data_embed_dict = dict()
            half_leave_list.append(user_id)

        list_idx = 0
        idx = -1
        for _keydict in search_dict:
            for __key in _keydict:
                idx += 1
                if __key == key:
                    data_dict['DISCORD_ID'] = "user.id"
                    data_embed_dict['DISCORD_ID'] = str("user.id")

                    for i in search_list[key]:
                        __data = await embeds.desc_ctx_input(ctx, bot, i, _keydict[key][i]['CONTENT'],
                                user = user, type = _keydict[key][i]['TYPE'])
                        data.append(__data)
                        data_embed_dict[i] = __data
                        data_dict[i] = "data[" + str(list_idx) + "]"
                        list_idx+=1
                    await embeds.send_success_embed(ticket_channel, 'Profile Updated', '')

                    try:
                        exec(SQLITE.sqlite_delete_row('cur', key, 'DISCORD_ID', 'user.id'))
                        exec(SQLITE.create_sqlite_cmd('cur', key, data_dict))
                        conn.commit()
                    except Exception as err:
                        raise Exception('SQLite Error: ' + str(err))

                    logger.success('Profile updated successfully.')
                    return
    except Exception as err:
        raise Exception('_update: ' + str(err))

    logger.success('~_update executed successfully.')

@bot.command()
async def update(ctx):
    logger.info('~update called for ' + str(ctx.author.id) + '/' + ctx.author.name)
    conn = sqlite3.connect('db/profile.sqlite')
    cur = conn.cursor()

    global base_dict
    global role_dict
    user_id = str(ctx.author.id)
    try:
        await ctx.message.delete()
        welcome_embed = await embeds.initialize_embed(ctx, ctx.author)
        exec(SQLITE.sqlite_exist_in_table('cur', 'MAIN', 'DISCORD_ID', 'ctx.author.id'))
        if not cur.fetchone()[0]:
            await embeds.error_title_embed(ctx, 'Not Found', 'User ' + str(ctx.author.mention) + ' not found in the DB.\nPlease append the data first.')
            logger.error(str(ctx.author.id) + '/' + ctx.author.name + " not found in the DB.")
            return

        _updated_roles = {i.name.upper() for i in ctx.author.roles}.intersection({role.upper() for role in role_list})
        possible_keys = {1: 'MAIN'}
        possible_keys.update({j : role for j, role in zip(range(2, 10000), _updated_roles)})
        rxn = await embeds.send_take_reaction(ctx, 'Profile Update', 'Please react on the profile that you need to update.\n', possible_keys, bot)

        await _update(ctx, ctx.author, possible_keys[rxn])
        await __profile(ticket_channel, ctx.author, None, True)
        await welcome_embed.delete()
    except Exception as err:
        await welcome_embed.delete()
        logger.error('~update: ' + str(err))
        return

    await embeds.send_success_embed(ctx, 'Profile updated successfully.', '')
    logger.success('~updated executed successfully.')
    for j in half_leave_list:
            full_day="ME"
            morning="M"
            evening="E"
            try:
                cur.execute('''SELECT Time FROM Attendance_DB WHERE  Attendance_DB.User_ID= ? AND Attendance_DB.Date=?''',[j,current_date])
                leave=str(cur.fetchone())
            except Exception as err:
                logger.error(err.__class__ + " " + str(err))

            bad_chars = ['(', ')', ',', "'"]
            for i in bad_chars:
                leave=leave.replace(i, '')

            if (leave.count(full_day)>0):
                logger.info("present full day")
            elif(leave.count(morning)==0):
                logger.info("present in morning")
            elif(leave.count(evening)==0):
                username = await bot.fetch_user(j)
                evening_leave_list=evening_leave_list+str(username)+"\n"

    leave_Embed.add_field(name='Users list absent in evening :', value = evening_leave_list+"\n\n\n", inline=False)
    await ctx.send(embed = leave_Embed,delete_after=1200.0)
    logger.info("'~absentees_evening' done successfully.")

#manual mark specific
# Attendance Leave Info #TODO: add kore properties
@bot.command()
async def attendance(ctx, *args):
    logger.info('~attendance is called by: ' + str(ctx.author.id) + '/' + ctx.author.name)
    author_role = ctx.author.roles
    for i in author_role:
        if str(i)=="Kore":
            role=str(i)
            break;
        else:
            role="Koders"

    if str(role) != "Kore" and args:
    #if str(ctx.author.roles[2]) != "Koders" and args:
        not_access_embed=discord.Embed(title="Sorry You dont have access to view others attendance!",description="",colour=0x11806a)
        await ctx.send(embed=not_access_embed,delete_after=60)
        logger.warning(str(ctx.author.id)+" dont have access")
        await ctx.message.delete()
        return

    start_date, end_date = await embed.data_input(ctx,bot)

    # TODO - set index accordingly to roles only
    # TODO - koders needs to be changed to Kore

    if not args: #check all attendances
        users = []
        if str(role) == "Kore":
            users=await member_loader()

            await embed.leave_and_attendance(ctx, bot, start_date, end_date, users, 2)
        elif str(role) != "Kore":
            users.append(str(ctx.author.id))
            await embed.leave_and_attendance(ctx, bot, start_date, end_date, users, 2)
    else:
        users = []
        for arg in args:
            arg:discord.Member
            users.append(str(arg.strip("!@<>")))
        await embed.leave_and_attendance(ctx, bot, start_date, end_date, users, 2)
    await ctx.message.delete()



@bot.command() #FIXME
async def export_leaves(ctx):
    logger.info(str(ctx.author.name))
    author_role = ctx.author.roles
    role = ''
    for i in author_role:
        if str(i)=="Kore":
            role=str(i)
            break;
          logger.info(str(user) + ", "+str(shift_status)+" - attendance marked")
          channel = await user.create_dm()
          date_time = datetime.datetime.now()
          embed = EMBEDS.attendance_dm(date_time.strftime("%D"), date_time.strftime("%H:%M:%S"), date_time.strftime("%A"))
          embed.add_field(name='Attendance marked for:', value = "Morning shift"+"\n\n\n", inline=False)
          await channel.send(embed=embed)
          await ctx.send(embed=embed,delete_after=30)

        else:
          else_embed=discord.Embed(title="Sorry attendance already marked",description="",colour=0x11806a)
          end=await ctx.send(embed=else_embed,delete_after=60)
          logger.warning(str(user.id)+" already marked")
    elif check_opening_time.hour > 14:
        else_embed=discord.Embed(title="Sorry time limit reached",description="",colour=0x11806a)
        end=await ctx.send(embed=else_embed,delete_after=60)
        logger.warning(str(user.id)+" time limit reached")


            role="Koders"
    if str(role) != "Kore" :
        not_access_embed=discord.Embed(title="Sorry You dont have access to view others leaves!",description="",colour=0x11806a)
        await ctx.send(embed=not_access_embed,delete_after=60)
        logger.warning(str(ctx.author.id)+" dont have access")
        return

    start_date, end_date = await embed.data_input(ctx,bot)
    await embed.export_csv(ctx,start_date,end_date)
    await ctx.message.delete()


async def _status(ctx, user):
    roles = {'KORE', 'KODERS', 'KOMMUNITY'}
#manual mark specific
@bot.command()
@commands.has_any_role("Kore")
async def mark_attendance(ctx):
    logger.info("Mark attendance function called")

    if not roles.intersection({i.name.upper() for i in user.roles}):
        await embeds.error_title_embed(ctx, '', user.mention+ ' is not active any more.')
        return
    await embeds.send_success_embed(ctx, '', user.mention + ' is currently active.')

@bot.command()
async def status(ctx, *, user_mentions):
    await ctx.message.delete()
    logger.info('~status called.')
    try:
        user_list = user_mentions.split()
        guild = ctx.author.guild
    check_opening_time=datetime.datetime.now()
    conn = sqlite3.connect('db/ATTENDANCE.sqlite')
    cur = conn.cursor()
    today=datetime.date.today()
    current_date = today.strftime("%Y-%m-%d")
    print(check_opening_time.hour)
    #TODO change time in prodcution
    if check_opening_time.hour < 15 and check_opening_time.hour >=11:
        shift_status="M"
    elif check_opening_time.hour < 19 and check_opening_time.hour >= 15:
        shift_status="E"

    try:
        cur.execute('''SELECT PRESENTEES,ABSENTEES FROM Attendance_table WHERE DATE = ? AND SHIFT = ?''', [current_date,shift_status])
        users = (cur.fetchone())

    except Exception as err:
        logger.error("error fetching detail " + str(err))

    if(str(users)=="None"):
        logger.error("No content found")
    elif(str(users[1])=="{No Absentees}"):
        logger.error("No Absentees found")
        no_absentees_embed=discord.Embed(title="No Absentees found on Date: "+str(current_date),description="",colour=0x11806a)
        await ctx.send(embed=no_absentees_embed,delete_after=20)
    else:
     presentees=set(users[0][1:-1].split(', '))
     absentees=set(users[1][1:-1].split(', '))
     absentees_dict =dict()
     absentees_string=""
     idx=1

     for absentee in absentees:
        absentees_dict[idx]=absentee
        absentees_string += str(idx)+" - "+ str(await bot.fetch_user(int(absentee))) + "\n"
        idx +=1

     user_list_embed = EMBEDS.simple_embed('Absentees list for Date: '+current_date, 'Choose the numbers(space seperated) corresponding to the users to mark attendance.' + '\n\n' + absentees_string)
     sent = await ctx.send(embed = user_list_embed)
     user_list = await EMBEDS.ctx_input(ctx, bot, sent)
     if not user_list:
        logger.error('User list timed out.')
        await ctx.message.delete()
        return
     user_list = list(map(int, user_list.split()))
     for i in user_list:
        if i < 1 or i >= idx:
            logger.error('Invalid index ' + str(i))
            await ctx.message.delete()
            return

     for i in user_list:
        presentees.add((absentees_dict[i]))
        user=await bot.fetch_user(int(absentees_dict[i]))
        channel = await user.create_dm()
        date_time = datetime.datetime.now()
        embed = EMBEDS.attendance_dm(date_time.strftime("%D"), date_time.strftime("%H:%M:%S"), date_time.strftime("%A"))
        embed.add_field(name='(M-morning shift , E-evening shift)', value ="Your attendance marked for: "+str(shift_status), inline=False)
        await channel.send(embed=embed)
        embed.add_field(name='Username', value =user, inline=False)
        await ctx.send(embed=embed,delete_after=30)

        absentees.remove(absentees_dict[i])
        logger.info("dm sent to "+str(user))

     try:
       if not absentees:
           absentees.add("No Absentees")
       cur.execute('''UPDATE Attendance_table SET PRESENTEES = ? , ABSENTEES = ? WHERE DATE = ? AND SHIFT = ?''', [str(presentees).replace("'",""),str(absentees).replace("'",""), current_date,shift_status ])
       conn.commit()
       logger.warning("changes made to db")
     except Exception as err:
      logger.error(err.__class__ + " " + str(err))
     await ctx.message.delete()
          logger.info(str(user) + ", "+str(shift_status)+" - attendance marked")
          channel = await user.create_dm()
          date_time = datetime.datetime.now()
          embed = EMBEDS.attendance_dm(date_time.strftime("%D"), date_time.strftime("%H:%M:%S"), date_time.strftime("%A"))
          embed.add_field(name='Attendance marked for:', value = "Evening shift"+"\n\n\n", inline=False)
          await channel.send(embed=embed)
          await ctx.send(embed=embed,delete_after=30)

        else:
            if((status.count(full_day)>0)):
                else_embed=discord.Embed(title="already marked",description="",colour=0x11806a)
                end=await ctx.send(embed=else_embed,delete_after=60)
                logger.warning(str(user.id)+" time limit reached")
            elif((status.count(morning)>0) and (status.count(evening)==0)):
               status = status + shift_status
               status = str(status)
               try:
                cur.execute('''UPDATE Attendance_DB SET Time = ? WHERE User_ID = ? AND Date = ?''', [status, str(user.id),current_date ])
                conn.commit()
               except Exception as err:
                logger.error(err.__class__ + " " + str(err))

               logger.warning(str(user)+", "+str(shift_status)+" - attendance updated")
               channel = await user.create_dm()
               date_time = datetime.datetime.now()
               embed = EMBEDS.attendance_dm(date_time.strftime("%D"), date_time.strftime("%H:%M:%S"), date_time.strftime("%A"))
               embed.add_field(name='Attendance marked for:', value = "Evening shift"+"\n\n\n", inline=False)
               await channel.send(embed=embed)
               await ctx.send(embed=embed,delete_after=30)
   elif check_opening_time.hour > 18:
        else_embed=discord.Embed(title="Sorry time limit reached",description="",colour=0x11806a)
        end=await ctx.send(embed=else_embed,delete_after=60)
        logger.warning(str(user.id)+" time limit reached")

# check all user leaves
@bot.command()
@commands.has_any_role("@Kore")
async def check_leaves(ctx):
    logger.info("Check leaves function called")
    start_date_embed=discord.Embed(title="Enter start date",description="Please enter in this format only 'yyyy-mm-dd'",colour=0x11806a)
    start=await ctx.send(embed=start_date_embed,delete_after=60)
    start_date1 = await embed.ctx_input(ctx, bot, start)
    if not start_date1:
        return

    end_date_embed=discord.Embed(title="Enter end date",description="Please enter in this format only 'yyyy-mm-dd'",colour=0x11806a)
    end=await ctx.send(embed=end_date_embed,delete_after=60)
    end_date1 = await embed.ctx_input(ctx, bot, end)
    if not end_date1:
        return


    start_date = datetime.datetime.strptime(start_date1, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date1, '%Y-%m-%d')

    conn = sqlite3.connect('Attendance_DB.sqlite')
    cur = conn.cursor()



    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    leave_Embed=embed.simple_embed(title="Absent Users\n",description="")


    for single_date in daterange(start_date, end_date):
        dates=str(single_date.strftime("%Y-%m-%d"))
        full_leave_list=""
        full_leave_list=full_leave_list+"\n𝗗𝗔𝗧𝗘: "+dates+"\n\n"

        morning_leave_list=""
        morning_leave_list=morning_leave_list+"\n𝗗𝗔𝗧𝗘: "+dates+"\n\n"

        evening_leave_list=""
        evening_leave_list=evening_leave_list+"\n𝗗𝗔𝗧𝗘: "+dates+"\n\n"



        #full leave
        try:
            cur.execute('''SELECT DISTINCT Users_DB_Attendance.User_ID FROM Users_DB_Attendance WHERE NOT EXISTS (SELECT Attendance_DB.User_ID FROM Attendance_DB WHERE Users_DB_Attendance.User_ID = Attendance_DB.User_ID AND Attendance_DB.Date = ?)''', [dates])
            full_absent = cur.fetchall()
        except Exception as err:
            logger.error(err.__class__ + " " + str(err))


        for i in full_absent:
            user_id=str(i)
            bad_chars = ['(', ')', ',', "'"]
            for i in bad_chars:
                user_id=user_id.replace(i, '')

            username = await bot.fetch_user(user_id)
            full_leave_list=full_leave_list+str(username)+"\n"

        leave_Embed.add_field(name='Users absent full day:', value = full_leave_list+"\n\n\n", inline=False)


        #half leave
        half_leave_list=[]
        try:
            cur.execute('''SELECT DISTINCT Users_DB_Attendance.User_ID FROM Users_DB_Attendance WHERE (SELECT Attendance_DB.User_ID   FROM Attendance_DB WHERE Users_DB_Attendance.User_ID=Attendance_DB.User_ID AND Attendance_DB.Date=? ) ''',[dates])
            half_absent = cur.fetchall()
        except Exception as err:
            logger.error(err.__class__ + " " + str(err))


        for i in half_absent:
            user_id=str(i)
            bad_chars = ['(', ')', ',', "'"]
            for i in bad_chars:
                user_id=user_id.replace(i, '')

            half_leave_list.append(user_id)

        for j in half_leave_list:
            full_day="ME"
            morning="M"
            evening="E"
            try:
                cur.execute('''SELECT Time FROM Attendance_DB WHERE  Attendance_DB.User_ID= ? AND Attendance_DB.Date=?''',[j,dates])
                leave=str(cur.fetchone())
            except Exception as err:
                logger.error(err.__class__ + " " + str(err))

            bad_chars = ['(', ')', ',', "'"]
            for i in bad_chars:
                leave=leave.replace(i, '')

            if (leave.count(full_day)>0):
                logger.info("present full day")
            elif(leave.count(morning)==0):
                username = await bot.fetch_user(j)
                morning_leave_list=morning_leave_list+str(username)+"\n"
            elif(leave.count(evening)==0):
                username = await bot.fetch_user(j)
                evening_leave_list=evening_leave_list+str(username)+"\n"

        leave_Embed.add_field(name='User absent in 1st half(Morning):', value = morning_leave_list+"\n\n\n", inline=False)
        leave_Embed.add_field(name='User absent in 2nd half(Evening):', value = evening_leave_list+"\n\n\n", inline=False)

    await ctx.send(embed=leave_Embed,delete_after=90)
    logger.warning("full leaves sent")

#Specific user leave
@bot.command()
async def specific_leaves(ctx, *,user: discord.Member):
    logger.info("specific leaves function called")
    user_author = ctx.author.id
    check_user = user.id
    check_username=ctx.author.name
    author_role = ctx.author.roles
    #print(author_role)

    if user_author == check_user:
        start_date_embed=discord.Embed(title="Enter start date",description="Please enter in this format only 'yyyy-mm-dd'",colour=0x11806a)
        start=await ctx.send(embed=start_date_embed,delete_after=60)
        start_date1 = await embed.ctx_input(ctx, bot, start)
        if not start_date1:
            logger.error("'start_date' timed out.")
            return

        end_date_embed=discord.Embed(title="Enter end date",description="Please enter in this format only 'yyyy-mm-dd'",colour=0x11806a)
        end=await ctx.send(embed=end_date_embed,delete_after=60)
        end_date1 = await embed.ctx_input(ctx, bot, end)
        if not end_date1:
            logger.error("'end_date' timed out.")
            return

        start_date = datetime.datetime.strptime(start_date1, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date1, '%Y-%m-%d')
        leaves=embed.show_leaves(start_date,end_date,check_user,check_username)
        await ctx.send(embed=leaves, delete_after = 90)
        logger.warning(str(check_username)+" leaves shown")

    if user_author != check_user:
        role=""
        for i in author_role:
            if str(i)=="kore":
                role=str(i)
                break;
            else:
                role="not admin"

        if role=="kore":

            start_date_embed=discord.Embed(title="Enter start date",description="Please enter in this format only 'yyyy-mm-dd'",colour=0x11806a)
            start=await ctx.send(embed=start_date_embed,delete_after=60)
            start_date1 = await embed.ctx_input(ctx, bot, start)
            if not start_date1:
                logger.error("'start_date1' timed out.")
                return

            end_date_embed=discord.Embed(title="Enter end date",description="Please enter in this format only 'yyyy-mm-dd'",colour=0x11806a)
            end=await ctx.send(embed=end_date_embed,delete_after=60)
            end_date1 = await embed.ctx_input(ctx, bot, end)
            if not end_date1:
                logger.error("'end_date1' timed out.")
                return

            start_date = datetime.datetime.strptime(start_date1, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date1, '%Y-%m-%d')
            leaves=embed.show_leaves(start_date,end_date,check_user,check_username)
            await ctx.send(embed=leaves, delete_after = 90)
            logger.warning(str(check_username)+" leaves shown")

        else:
            end_date_embed=discord.Embed(title="Sorry You dont have access to view others leaves!",description="",colour=0x11806a)
            end=await ctx.send(embed=end_date_embed,delete_after=60)
            logger.warning(str(user_author)+" dont have access")


# Attendance Leave Info
@bot.command()
async def check_attendance(ctx, *,user: discord.Member):
    logger.info("check attendance called")
    user_author = ctx.author.id
    check_user = user.id
    check_username=ctx.author.name
    author_role = ctx.author.roles
    #print(author_role)

    if user_author == check_user:
        start_date_embed=discord.Embed(title="Enter start date",description="Please enter in this format only 'yyyy-mm-dd'",colour=0x11806a)
        start=await ctx.send(embed=start_date_embed,delete_after=60)
        start_date1 = await embed.ctx_input(ctx, bot, start)
        if not start_date1:
            logger.error("'start_date1' timed out.")
            return

        end_date_embed=discord.Embed(title="Enter end date",description="Please enter in this format only 'yyyy-mm-dd'",colour=0x11806a)
        end=await ctx.send(embed=end_date_embed,delete_after=60)
        end_date1 = await embed.ctx_input(ctx, bot, end)
        if not end_date1:
            logger.error("'end_date1' timed out.")
            return

        start_date = datetime.datetime.strptime(start_date1, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date1, '%Y-%m-%d')
        attendance,save_filename=embed.show_attendance(start_date,end_date,check_user,check_username)
        await ctx.send(embed=attendance,file=discord.File(save_filename), delete_after = 90)
        logger.warning(str(check_username)+" Attendace shown")

    if user_author != check_user:
        role=""
        for i in author_role:
            if str(i)=="kore":
                role=str(i)
                break;
            else:
                role="not admin"


        if role=="kore":
            start_date_embed=discord.Embed(title="Enter start date",description="Please enter in this format only 'yyyy-mm-dd'",colour=0x11806a)
            start=await ctx.send(embed=start_date_embed,delete_after=60)
            start_date1 = await embed.ctx_input(ctx, bot, start)
            if not start_date1:
                logger.error("'start_date1' timed out.")
                return

            end_date_embed=discord.Embed(title="Enter end date",description="Please enter in this format only 'yyyy-mm-dd'",colour=0x11806a)
            end=await ctx.send(embed=end_date_embed,delete_after=60)
            end_date1 = await embed.ctx_input(ctx, bot, end)
            if not end_date1:
                logger.error("'end_date1' timed out.")
                return

            start_date = datetime.datetime.strptime(start_date1, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date1, '%Y-%m-%d')
            attendance=embed.show_attendance(start_date,end_date,check_user,check_username)
            await ctx.send(embed=attendance, delete_after = 90)
            logger.warning(str(check_username)+" Attendace shown")
        else:
            end_date_embed=discord.Embed(title="Sorry You dont have access to view others attendance!",description="",colour=0x11806a)
            end=await ctx.send(embed=end_date_embed,delete_after=60)
            logger.warning(str(user_author)+" dont have access")

@loop(minutes=1)
async def attendance_task():
    await bot.wait_until_ready()
    channel = bot.get_channel(int(os.environ.get('CHANNEL_ID')))  # TODO  - Add koders' channel id
    working_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    date_time = datetime.datetime.now()
    for working_day in working_days:
        if working_day == date_time.strftime("%A") and date_time.strftime("%H:%M") == "11:00":
            logger.info("Ran morning attendance.")
            await take_attendance(channel, "11:00", "11:20")
        if working_day == date_time.strftime("%A") and date_time.strftime("%H:%M") == "15:00":
            logger.info("Ran post lunch attendance.")
            await take_attendance(channel, "15:00", "15:20")
    logger.info("Waiting for tasks...")

        user_dict = {i.id : i for i in guild.members}
        users = {user_dict[int(user[3:-1])] for user in user_list}

        for user in users:
            await _status(ctx, user)
    except Exception as err:
        logger.error(err)
        return
    logger.success('~status executed successfully.')
async def run_schedules():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)

if __name__ == '__main__':
    try:
        environ_check('TOKEN')
        bot.run(os.environ.get('TOKEN'))
    except Exception as err:
        logger.error('Exception at main worker\n' + str(err))
    except Exception as _err:
        logger.error("Exception found at profile worker.\n" + str(_err))
    issue_embed=embeds.simple_embed(ctx, title="Issues List:",description=list)
    message  = await ctx.send(embed = issue_embed,delete_after=60)

# Main driver
if __name__ == "__main__":
    try:
        load_dotenv(find_dotenv())
        init_schedules()
        client.loop.create_task(run_schedules())
        client.run(os.environ.get('TOKEN'))
    except CommandNotFound:
        pass  # For handling command not found errors
        attendance_task.start()
        bot.run(os.environ.get("TOKEN"))

    except discord.ext.commands.errors.MissingAnyRole as e:
        logger.warning('~' + e)
    except Exception as _e:
        logger.warning("Exception found at main worker. Reason: " + str(_e), exc_info=True)
