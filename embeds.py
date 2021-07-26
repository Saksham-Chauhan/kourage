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

logger = Logger("kourage-work")

def simple_embed(title, description):
    embed = discord.Embed(
            title = title,
            description = description,
            colour=0x28da5b
            )
    #embed.thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text="Made with ❤️️  by Koders")
    return embed

def error_embed(title, description):
    embed = discord.Embed(
            title = title,
            description = description,
            colour=0xB33F40
            )
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text="Made with ❤️️  by Koders")
    return embed

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
        return ret, _embed

    except asyncio.TimeoutError:
        await _embed.delete()
        return None, None

def validate_name(name):
    for letter in name:
        if letter in "0123456789" or len(name) < 3 or len(name.split()) > 3:
            return False
    return True

def validate_phone(phone):
    for num in phone:
        if num not in "+ ()0123456789":
            return False
    return True

def validate_email(email):
    regex = "^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$"
    if re.search(regex, email):
        return True
    else:
        return False

async def ctx_input(ctx, bot, embed, timeout = 60.0, user = None, type = None):
    types = [None, "name", "phone", "email"]
    try:
        if type not in types:
            await embed.delete()
            err_embed = error_embed("", "Some technical issue occured.\nIf you are an admin please look into the log files.")
            await ctx.send(embed = err_embed, delete_after = timeout)
            logger.error("Invalid token type '" + type + "' given for ctx input.")
            return
        if type:
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
            if type:
                if not eval (cmd.format(msg = _id)):
                    await msg.delete()
                    raise Exception("Invalid token '" + _id + "' for type '" + type + "'.")
            await msg.delete()
            return _id

    except asyncio.TimeoutError as err:
        await embed.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = timeout)
        return None

    except Exception as err:
        txt = str(err)
        print(err.__context__)
        _err_embed = error_embed("", txt)
        await ctx.send(embed = _err_embed, delete_after = timeout)
        return None
