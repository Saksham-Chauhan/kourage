import platform
import time
import discord
import asyncio
import datetime
from colorama import init
from termcolor import colored

machine = platform.node()
init()


class Logger:
    def __init__(self, app):
        self.app = app

    def info(self, message):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', 'yellow'))

    def warning(self, message):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', 'green'))

    def error(self, message):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', 'red'))

    def color(self, message, color):
        print(colored(f'[{time.asctime(time.localtime())}] [{machine}] [{self.app}] {message}', color))


logger = Logger("kourage-feedback")


def simple_embed(title, description):
    embed = discord.Embed(
        title=title,
        description=description,
        colour=0x11806a
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/719103754502275083/869946597004435466/81-813600_feedback-icon-png"
            "-white-chat-2.png")
    embed.set_footer(text="Made with ❤️️  by Koders")
    embed.timestamp = datetime.datetime.utcnow()
    return embed


_rxn_no = {'1️⃣': 1, '2️⃣': 2, '3️⃣': 3, '4️⃣': 4}
_rxn = {'😍': 1, '🙂': 2, '😑': 3, '😕': 4, '😡': 5}
_rxn_NA = {'❌': 1, '✅': 2}


async def take_reaction_no(ctx, rxn_amnt, _embed, bot, timeout=300.0):
    rxn = dict()
    _i = 1
    for i in _rxn_no:
        if _i > rxn_amnt:
            break
        rxn[i] = _i
        _i += 1

    for i in rxn:
        await _embed.add_reaction(i)

    def check(reaction, user):
        _c1 = user.bot is not True and user == ctx.author
        return _c1 and str(reaction.emoji) in rxn

    try:
        result = await bot.wait_for('reaction_add', check=check, timeout=timeout)
        reaction, user = result

        ret = (None, rxn[str(reaction)])[str(reaction) in rxn]
        return ret, _embed

    except asyncio.TimeoutError:
        await ctx.delete()


async def take_reaction(ctx, rxn_amnt, _embed, bot, timeout=300.0):
    rxn = dict()
    _i = 1
    for i in _rxn:
        if _i > rxn_amnt:
            break
        rxn[i] = _i
        _i += 1

    for i in rxn:
        await _embed.add_reaction(i)

    def check(reaction, user):
        _c1 = user.bot is not True and user == ctx.author
        return _c1 and str(reaction.emoji) in rxn

    try:
        result = await bot.wait_for('reaction_add', check=check, timeout=timeout)
        reaction, user = result

        ret = (None, rxn[str(reaction)])[str(reaction) in rxn]
        return ret, _embed

    except asyncio.TimeoutError:
        await ctx.delete()


async def take_reaction_NA(ctx, rxn_amnt, _embed, bot, timeout=300.0):
    rxn = dict()
    _i = 1
    for i in _rxn_NA:
        if _i > rxn_amnt:
            break
        rxn[i] = _i
        _i += 1

    for i in rxn:
        await _embed.add_reaction(i)

    def check(reaction, user):
        _c1 = user.bot is not True and user == ctx.author
        return _c1 and str(reaction.emoji) in rxn

    try:
        result = await bot.wait_for('reaction_add', check=check, timeout=timeout)
        reaction, user = result

        ret = (None, rxn[str(reaction)])[str(reaction) in rxn]
        return ret, _embed

    except asyncio.TimeoutError:
        await ctx.delete()


async def ctx_input(ctx, bot, embed, timeout=60.0):
    try:
        msg = await bot.wait_for(
            "message",
            timeout=timeout,
            check=lambda message: message.author == ctx.author
        )

        if msg:
            await embed.delete()
            _id = msg.content
            await msg.delete()
            return _id

    except asyncio.TimeoutError:
        await embed.delete()
        await ctx.send('Cancelling due to timeout.', delete_after=timeout)
        return None
