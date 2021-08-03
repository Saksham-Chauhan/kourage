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

if __name__ == '__main__':
    try:
        environ_check('TOKEN')
        bot.run(os.environ.get('TOKEN'))
    except Exception as err:
        logger.error('Exception at main worker\n' + str(err))
