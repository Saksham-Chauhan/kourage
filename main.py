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
    logger.error(error)

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

    logger.success('~__profile executed successfully.')

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

        for user in user_list:
            users.add(await bot.fetch_user(int(user[3 : -1])))

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

        data = list()
        data_dict = dict()
        data_embed_dict = dict()

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

async def _status(ctx, user):
    roles = {'KORE', 'KODERS', 'KOMMUNITY'}

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

        user_dict = {i.id : i for i in guild.members}
        users = {user_dict[int(user[3:-1])] for user in user_list}

        for user in users:
            await _status(ctx, user)
    except Exception as err:
        logger.error(err)
        return
    logger.success('~status executed successfully.')

if __name__ == '__main__':
    try:
        environ_check('TOKEN')
        bot.run(os.environ.get('TOKEN'))
    except Exception as _err:
        logger.error("Exception found at profile worker.\n" + str(_err))
