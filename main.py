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
from discord.ext import commands

import embeds
import rules
import client
import career
import partner
import archive as ARCHIVE

#################################################
#                   GLOBALS                     #
#################################################
#                                               #
bot = commands.Bot(command_prefix="~")          #
logger = embeds.Logger("kourage-onboarding")    #
                                                #
message_ids = {                                 #
        866592404891238400 : 'rules',           #
        866665183468060692 : 'client',          #
        867370078349557760 : 'career',          #
        866668351026364456 : 'partner'          #
        }                                       #
                                                #
admin_id = 511138541724631050                   #
admin_channel = None                            #
discord_key = None                              #
rules_ticket_channel = None                     #
client_ticket_channel = None                    #
career_ticket_channel = None                    #
partner_ticket_channel = None                   #
#################################################

def environ_check(var):
    if not var in os.environ:
        raise Exception("'" + var + "' not found in the environ list.")

#################################################
#               on_ready event                  #
#################################################
@bot.event
async def on_ready():
    try:
        global admin_channel
        global career_ticket_channel
        global client_ticket_channel
        global discord_key
        global partner_ticket_channel

        environ_check('ADMIN_CHANNEL_ID')
        environ_check('CAREER_TICKET_CHANNEL_ID')
        environ_check('CLIENT_TICKET_CHANNEL_ID')
        environ_check('DISCORD_KEY')
        environ_check('PARTNER_TICKET_CHANNEL_ID')

        admin_channel = bot.get_channel(int(os.environ.get('ADMIN_CHANNEL_ID')))
        career_ticket_channel = bot.get_channel(int(os.environ.get('CAREER_TICKET_CHANNEL_ID')))
        client_ticket_channel = bot.get_channel(int(os.environ.get('CLIENT_TICKET_CHANNEL_ID')))
        discord_key = bot.get_channel(os.environ.get('DISCORD_KEY'))
        partner_ticket_channel = bot.get_channel(int(os.environ.get('PARTNER_TICKET_CHANNEL_ID')))

        logger.info('Admin Channel: ' + str(admin_channel.id) + "/" + admin_channel.name)
        logger.info('Career Ticket Channel: ' + str(career_ticket_channel.id) + "/" + career_ticket_channel.name)
        logger.info('Client Ticket Channel: ' + str(client_ticket_channel.id) + "/" + client_ticket_channel.name)
        logger.info('Partner Ticket Channel: ' + str(partner_ticket_channel.id) + "/" + partner_ticket_channel.name)
        


    except Exception as err:
        logger.error("Error in '~on_ready': " + str(err))
        return

    db = sqlite3.connect('Career_DB.sqlite')
    cursor = db.cursor()
    try:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Career(
            Role TEXT,
            Discord_Id TEXT,
            Name TEXT,
            Phone INTEGER,
            Mail TEXT,
            Resume TEXT
            )
        ''')
    except Exception as err:
        logger.error('SQLite error: ' + err)
        return

    logger.success("Kourage is running at version {0}".format("0.1.0"))

#################################################
#           on_raw_reaction_add                 #
#################################################
@bot.event
async def on_raw_reaction_add(ctx):
    user = ctx.member

    if user.bot is True or ctx.message_id not in message_ids:
        return

    try:
    #if True:
        cmd = message_ids[ctx.message_id] + ".on_react" + \
            "(bot, bot.get_channel(" + str(ctx.channel_id) + "), user, " + \
            message_ids[ctx.message_id] + "_ticket_channel, logger)"
        await eval(cmd)
    except Exception as err:
        logger.error("'on_react': " + str(err))
        return
    logger.success("on_raw_reaction_add executed successfully.")

# User Info Command
@bot.command()
async def info(ctx, *,user: discord.Member):
    logger.info('~info called by ' + str(ctx.author.id) + ' for ' + str(user.id))

    conn = sqlite3.connect('Career_DB.sqlite')
    cur = conn.cursor()

    infoEmbed = discord.Embed(
        colour=0x28da5b,
        title='User Profile',
        description=''' All the user related information i.e.,
        -Name
        -Mobile number
        -Email id ,etc. '''
    )
    infoEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    infoEmbed.set_footer(text="Made with ❤️️  by Koders")
    infoEmbed.timestamp = datetime.datetime.utcnow()

    try:
        cur.execute('''SELECT Role, Name, Phone, Mail, Resume FROM Career WHERE Discord_Id = ?''', (user.id, ))
    except Exception as e:
        raise Exception('DB Error\n' + e.args[0])

    rows = cur.fetchone()
    field_name = ['Role', 'Name', 'Phone Number', 'Mail Id', 'Resume']

    if rows != None:
        for i in range(len(field_name)):
            infoEmbed.add_field(name=field_name[i], value=rows[i], inline=True)

        await ctx.send(embed=infoEmbed, delete_after = 80)

        # Sending Resume file
        files = glob.glob(rows[4])
        for i in files:
            await ctx.send(file = discord.File(i))

    else:
        no_userEmbed = discord.Embed(
            colour=0x28da5b,
            title='User Profile Not Found',
            description=" Sorry! This user profile does not exist in the database. "
        )
        no_userEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
        no_userEmbed.set_footer(text="Made with ❤️️  by Koders")
        no_userEmbed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=no_userEmbed, delete_after = 80)
        logger.info('User: ' + str(user.id) + '/' + str(user.name) + ' not found')

    await ctx.message.delete()
    cur.close()
    logger.success('~info executed successfully')

@bot.command()
async def shortlist(ctx,*argv):
    conn = sqlite3.connect('Career_DB.sqlite')
    cur = conn.cursor()
    message_embed=discord.Embed(title="",description="Please enter the message",colour=0x11806a)
    message=await ctx.send(embed=message_embed,delete_after=60)
    email_input = await embeds.ctx_input(ctx, bot, message)

    if not email_input:
        return

    for arg in argv:
        arg:discord.User
        user=str(arg)
        bad_chars = ['<', '>', '@', "!"]
        for i in bad_chars:
            user=user.replace(i, '')
        user_id=(user)
        message_input = email_input
        username = await bot.fetch_user(user)
        await username.send(message_input,delete_after=60)
        print("Message sent:"+str(username))

        cur.execute('''SELECT Mail FROM Career WHERE Discord_Id = ?''', [user_id])

        rows = cur.fetchone()
        email=str(rows)
        bad_chars = ['(', ')', ',', "'"]
        for i in bad_chars:
            email=email.replace(i, '')
        print(email)
        #email_file.send_Email(email,email_input)
        #print("email sent:"+str(username))

@bot.command()
async def reject(ctx,*argv):
    conn = sqlite3.connect('Career_DB.sqlite')
    cur = conn.cursor()
    message_embed=discord.Embed(title="",description="Please enter the message",colour=0x11806a)
    message=await ctx.send(embed=message_embed,delete_after=60)
    email_input = await embeds.ctx_input(ctx, bot, message)
    if not email_input:
        return
    for arg in argv:

        arg:discord.User
        user=str(arg)
        bad_chars = ['<', '>', '@', "!"]
        for i in bad_chars:
            user=user.replace(i, '')
        user_id=(user)
        message_input = email_input
        username = await bot.fetch_user(user)
        await username.send(message_input,delete_after=60)
        print("Message sent:"+str(username))

        cur.execute('''SELECT Mail FROM Career WHERE Discord_Id = ?''', [user_id])

        rows = cur.fetchone()
        email=str(rows)
        bad_chars = ['(', ')', ',', "'"]
        for i in bad_chars:
            email=email.replace(i, '')
        print(email)
        #email_file.send_Email(email,email_input)
        #print("email sent:"+str(username))

###
# archive
###
@bot.command()
async def archive(ctx):
    if ctx.author.id != admin_id:
        return
    try:
        logger.info('~archive called with backlogging to the admin channel: '+ admin_channel.name)
    except Exception as err:
        logger.error("'admin channel id' : " + str(err))
        return

    try:
        await ARCHIVE._archive(ctx.channel.id, admin_channel, bot, logger, True, discord_key)
        await ARCHIVE.__delete(ctx, logger)
    except Exception as err:
        logger.error(err)
        return

if __name__ == '__main__':
    try:
        environ_check('TOKEN')
        bot.run(os.environ.get('TOKEN'))
    except CommandNotFound as _err:
        logger.error("TOKEN not found.\n" + _err)
    except Exception as _err:
        logger.error("Exception found at main worker.\n" + str(_err))
