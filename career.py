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

logger = None

#############################################
# CLIENT_REACT
#############################################
async def on_react(bot, ctx, user, ticket_channel, _logger):
    global logger
    logger = _logger
    logger.info('~on_ready called for ' + str(user.id))
    cursor = sqlite3.connect('Career_DB.sqlite')
    role_dict = {1 : 'Design', 2 : 'Development', 3 : 'Content', 4 : 'Marketing'}

    welcome_embed = discord.Embed(
            title="TICKET CREATION",
            colour=0x11806a
            )
    welcome_embed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    welcome_embed.set_footer(text="Welcome to Koders ❤️️")
    welcome_embed.set_author(name = f'Bot initialized for  {user.name}', icon_url = f'{user.avatar_url}')
    welcome_embed.timestamp = datetime.datetime.utcnow()
    welcome=await ctx.send(embed=welcome_embed)

    apply_roleEmbed = discord.Embed(
        colour = 0x28da5b,
        title = 'In which role you wanted to apply at Koders?',
        description = '''Enter your interested role name.
        1. Design
        2. Developer
        3. Content
        4. Marketing'''
    )
    apply_roleEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    apply_roleEmbed.set_footer(text="Made with ❤️️  by Koders")
    apply_roleEmbed.timestamp = datetime.datetime.utcnow()

    apply_role = await ctx.send(embed = apply_roleEmbed)
    role_no, __tmp = await embeds.take_reaction(ctx, 4, apply_role, bot, user = user)
    if not role_no:
        await welcome.delete()
        raise Exception("'role' timed out.")
    await __tmp.delete()
    role = role_dict[role_no]
    logger.info("'role' input successful.")

    nameEmbed = discord.Embed(
        colour = 0x28da5b,
        title = 'What’s your good name?',
        description = " Write your full name."
    )
    nameEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    nameEmbed.set_footer(text="Made with ❤️️  by Koders")
    nameEmbed.timestamp = datetime.datetime.utcnow()

    name_sent = await ctx.send(embed = nameEmbed)
    name = await embeds.ctx_input(ctx, bot, name_sent, user = user, type = "name")
    if not name:
        await welcome.delete()
        raise Exception("'name' timed out.")
    logger.info("'name' input successful")

    contactEmbed = discord.Embed(
        colour = 0x28da5b,
        title = 'What is your contact number?',
        description = "Enter the number on which you can be contacted at any hour of the day. "
        )
    contactEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    contactEmbed.set_footer(text="Made with ❤️️  by Koders")
    contactEmbed.timestamp = datetime.datetime.utcnow()

    contact_sent = await ctx.send(embed = contactEmbed)

    contact = await embeds.ctx_input(ctx, bot, contact_sent, user = user, type = "phone")
    if not contact:
        await welcome.delete()
        raise Exception("'contact' timed out.")
    logger.info("'contact' input successful.")

    emailEmbed = discord.Embed(
        colour = 0x28da5b,
        title = 'Enter your official email id?',
        description = " Make sure it’s free of typos. "
    )
    emailEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    emailEmbed.set_footer(text="Made with ❤️️  by Koders")
    emailEmbed.timestamp = datetime.datetime.utcnow()

    email_sent = await ctx.send(embed = emailEmbed)
    email = await embeds.ctx_input(ctx, bot, email_sent, user = user, type = "email")
    if not email:
        await welcome.delete()
        raise Exception("'email' timed out.")
    logger.info("'email' input successful.")

    resumeEmbed = discord.Embed(
        colour = 0x28da5b,
        title = 'Submit your Resume in pdf form.',
        description = " Make sure it’s free of typos. "
    )
    resumeEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    resumeEmbed.set_footer(text="Made with ❤️️  by Koders")
    resumeEmbed.timestamp = datetime.datetime.utcnow()

    resume_sent = await ctx.send(embed = resumeEmbed)
    try:
        msg = await bot.wait_for(
            "message",
            timeout=300.0,
            check=lambda message: message.author == user
        )

        if msg:
            await resume_sent.delete()
            print("!")
            if not msg.attachments:
                await welcome.delete()
                raise Exception("Invalid resume.\nExpected a file, recieved '" + msg.content + "'")
            resume = msg.attachments[0].url
            await msg.delete()

    except asyncio.TimeoutError:
        await resume_sent.delete()
        await ctx.send('Cancelling due to timeout.', delete_after = 300)
        await welcome.delete()
        raise Exception("'resume' input timed out.")
    except Exception as err:
        err_embed = embeds.error_embed("", str(err))
        await msg.delete()
        await ctx.send(embed = err_embed, delete_after = 60)
        await welcome.delete()
        raise Exception(str(err))

    await welcome.delete()
    fname = str(user.id) + '.' + resume.split('.')[-1]
    _fname = "curl -o resumes/" + fname + ' ' + resume
    out = subprocess.Popen(_fname, shell = True, stdout = subprocess.DEVNULL, stderr = subprocess.STDOUT)
    resume = "resumes/" + fname
    user_id = user.id

    profileEmbed = discord.Embed(
        colour = 0x28da5b,
        title = 'User Profile',
        description = '''All the user related information i.e.,
        -Name
        -Mobile number
        -Email id ,etc.
        '''
    )
    profileEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    profileEmbed.set_footer(text="Made with ❤️️  by Koders")
    profileEmbed.timestamp = datetime.datetime.utcnow()

    profileEmbed.add_field(name='Applied Role', value = f'{role}', inline=True)
    profileEmbed.add_field(name='Name', value = f'{name}', inline=True)
    profileEmbed.add_field(name='Phone Number', value = f'{contact}', inline=True)
    profileEmbed.add_field(name='Mail Id', value = f'{email}', inline=True)
    profileEmbed.add_field(name='Resume', value = f'{resume}', inline=True)

    await ticket_channel.send(embed = profileEmbed)

    cursor.execute('''INSERT INTO Career
    (Role, Discord_Id, Name, Phone, Mail, Resume) VALUES (?, ?, ?, ?, ?, ?)''', (role, user_id, name, contact, email, resume))

    cursor.commit()
    cursor.close
    await ctx.send(user.mention + ", Thank you for filling out data. We'll get back to you soon", delete_after = 60)
    logger.success('Data written to DB successfully')
    logger.success("'~on_react' completed successfully")


