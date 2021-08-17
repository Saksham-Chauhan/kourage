import asyncio
import re
import json
import os
import logging
import platform
import time
import discord
from colorama import init
from termcolor import colored
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

logger = None

embed_color = {
        'info' : 0xefb701,
        'success' : 0x9af530,
        'error' : 0xb90000
        }

def desc_embed(description):
    embed = discord.Embed(
            title = '',
            description = description,
            colour=embed_color['info']
            )
    return embed
    
def title_embed(title, description, footer = True):
    embed = discord.Embed(
            title = title,
            description = description,
            colour=embed_color['info']
            )
    if footer:
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text="Made with ❤️️  by Koders")
    return embed

async def initialize_embed(ctx, user):
    embed = title_embed('Box Initialized for ' + user.name, '', footer=False)
    send = await ctx.send(embed = embed)
    return send

def error_embed(title, description):
    embed = discord.Embed(
            title = title,
            description = description,
            colour=embed_color['error']
            )
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text="Made with ❤️️  by Koders")
    return embed
    
def success_embed(title, desc):
    embed = discord.Embed(
            title = title,
            description = desc,
            color = embed_color['success']
            )
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text="Made with ❤️️  by Koders")
    return embed
    
async def send_success_embed(ctx, title, desc, timeout = 60.0):
    _embed = success_embed(title, desc)
    await ctx.send(embed = _embed, delete_after = timeout)

async def send_title_embed(ctx, title, description, timeout = None):
    embed = title_embed(title, description)
    return await ctx.send(embed = embed, delete_after = timeout)
    
async def error_title_embed(ctx, title, description, timeout = 60.0):
    embed = error_embed(title, description)
    sent = await ctx.send(embed = embed, delete_after = timeout)
    
def user_title_embed(title, user, description):
    avatar_url = user.avatar_url
    _embed = title_embed(title, description)
    _embed.set_thumbnail(usr = avatar_url)
    _embed.set_footer(text="Made with ❤️️  by Koders")
    _embed.timestamp = datetime.datetime.utcnow()
    return _embed
    
async def desc_ctx_input(ctx, bot, field, description, user = None, type = None):
    _embed = desc_embed(description)
    _sent = await ctx.send(embed = _embed)
    if user:
        _input = await ctx_input(ctx, bot, _sent, user = user, type = type)
    else:
        _input = await ctx_input(ctx, bot, _sent, user = ctx.user, type = type)
    if not _input:
        return await desc_ctx_input(ctx, bot, field, description, user, type)
    logger.info("'" + field + "' input successful.")
    return _input
    
async def desc_take_reaction(ctx, bot, desc, rxn_amount, field, timeout = 60.0, user = None):
    _embed = desc_embed(desc)
    _sent = await ctx.send(embed = _embed)
    
    rxn = await take_reaction(ctx, rxn_amount, _sent, bot, timeout = timeout, user = user)
    logger.info("'" + field + "' input successful.")
    return rxn

async def send_inline(channel, title, desc, _dict, timeout = None):
    _embed = title_embed(title, desc)
    for data in _dict:
        cmd = "_embed.add_field(name = '" + (' '.join(data.split('_'))).capitalize() + "', value = f'{_dict[data]}', inline = True)"
        eval(cmd)
    await channel.send(embed = _embed, delete_after = timeout)


_rxn = {'1️⃣' : 1, '2️⃣' : 2, '3️⃣' : 3, '4️⃣' : 4, '5️⃣' : 5, '6️⃣' : 6}

async def take_reaction(ctx, rxn_amnt, _embed, bot, timeout=60.0, user = None):
    rxn = dict()
    _i = 1
    for i in _rxn:
        if _i > rxn_amnt:
            break
        rxn[i] = _i
        _i += 1

    for i in rxn:
        await _embed.add_reaction(i)

    def check(reaction, _user):
        if user:
            _c1 = _user.bot is not True and _user == user
        else:
            _c1 = _user.bot is not True and _user == ctx.author
        return _c1 and str(reaction.emoji) in rxn

    try:
        result = await bot.wait_for('reaction_add', check=check, timeout=timeout)
        reaction, _user = result

        ret = (None, rxn[str(reaction)]) [ str(reaction) in rxn ]
        await _embed.delete()
        return ret

    except asyncio.TimeoutError as err:
        await _embed.delete()
        raise asyncio.TimeoutError(err)

async def send_take_reaction(ctx, title, desc, _dict, bot, timeout = 60.0, user = None):
    try:
        for i, j in zip(_rxn, _dict):
            desc += '\n' + i + " " + _dict[j]
        _embed = await send_title_embed(ctx, title, desc)
        return await take_reaction(ctx, len(_dict), _embed, bot, timeout = timeout, user = user)
    except asyncio.TimeoutError as err:
        await error_title_embed(ctx, 'TIMEOUT', 'Connection timed out.\nPlease try again later.')
        raise asyncio.TimeoutError(err)

def validate_name(name):
    for letter in name:
        if letter in "0123456789" or len(name) < 3 or len(name.split()) > 3:
            return False
    return True

def validate_phone(phone):
    for num in phone:
        if num not in "+() 0123456789":
            return False
    return True

def validate_email(email):
    regex = "^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$"
    if re.search(regex, email):
        return True
    else:
        return False
        
# TODO; redmine api format regex here.
def validate_api(api):
    return True

async def ctx_input(ctx, bot, embed, timeout = 60.0, user = None, type = None):
    types = [None, "None", "name", "phone", "email", "api"]
    try:
        if type not in types:
            await embed.delete()
            err_embed = error_embed("", "Some technical issue occured.\nIf you are an admin please look into the log files.")
            await ctx.send(embed = err_embed, delete_after = timeout)
            logger.error("Invalid token type '" + type + "' given for ctx input.")
            return
        if type and type != "None":
            cmd = ("validate_" + type + "(\'{msg}\')", "True") [not type]
        if user is None:
                check = lambda message: message.author == ctx.author
        else:
                check = lambda message: message.author == user
        msg = await bot.wait_for(
            "message",
            timeout=timeout,
            check = check
        )

        if msg:
            await embed.delete()
            _id = msg.content
            if type and type != "None":
                if not eval (cmd.format(msg = _id)):
                    await msg.delete()
                    raise Exception("Invalid token '" + _id + "' for type '" + type + "'.")
            await msg.delete()
            if(type == "api"):
                _id = base64.b64encode(_id.encode("ascii"))
                return _id
            return _id

    except asyncio.TimeoutError as err:
        await embed.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = timeout)
        raise asyncio.TimeoutError(err)

    except Exception as err:
        txt = str(err)
        _err_embed = error_embed("", txt)
        await ctx.send(embed = _err_embed, delete_after = timeout)
        return None
