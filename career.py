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
    welcome_embed = discord.Embed(
            title="TICKET",
            description = "You're almost there!\nPlease provide the following details.",
            colour=0x11806a
            )
    welcome_embed.set_thumbnail(url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    welcome_embed.set_footer(text="Welcome to Koders ❤️️")
    welcome_embed.set_author(name = f'Bot initialized for  {user.name}', icon_url = f'{user.avatar_url}')
    welcome_embed.timestamp = datetime.datetime.utcnow()
    welcome=await ctx.send(embed=welcome_embed)

    cursor = sqlite3.connect('Career_DB.sqlite')

    nameEmbed=discord.Embed(title="",description="What's your good name?",colour=0x11806a)
    name_sent = await ctx.send(embed = nameEmbed)
    name = await embeds.ctx_input(ctx, bot, name_sent, user = user, type = "name")
    if not name:
        await welcome.delete()
        raise Exception("'name' timed out.")
    logger.info("'name' input successful")

    addressEmbed=discord.Embed(title="",description="Please enter your address.",colour=0x11806a)
    address_sent = await ctx.send(embed = addressEmbed)
    address = await embeds.ctx_input(ctx, bot, address_sent, user = user)
    if not address:
        await welcome.delete()
        raise Exception("'address' timed out.")
    logger.info("'address' input successful")

    emailEmbed=discord.Embed(title="",description="Please provide your email-id.",colour=0x11806a)
    email_sent = await ctx.send(embed = emailEmbed)
    email = await embeds.ctx_input(ctx, bot, email_sent, user = user)
    if not email:
        await welcome.delete()
        raise Exception("'email' timed out.")
    logger.info("'email' input successful")

    contactEmbed=discord.Embed(title="",description="Please enter your contact number.",colour=0x11806a)
    contact_sent = await ctx.send(embed = contactEmbed)
    contact = await embeds.ctx_input(ctx, bot, contact_sent, user = user)
    if not contact:
        await welcome.delete()
        raise Exception("'contact' timed out.")
    logger.info("'contact' input successful")

    professionEmbed=discord.Embed(title="",description="Are you a college student or a working professional?",colour=0x11806a)
    profession_sent = await ctx.send(embed = professionEmbed)
    profession = await embeds.ctx_input(ctx, bot, profession_sent, user = user)
    if not profession:
        await welcome.delete()
        raise Exception("'profession' timed out.")
    logger.info("'profession' input successful")

    role_dict = {1 : 'Design', 2 : 'Development', 3 : 'Content', 4 : 'Marketing'}
    apply_roleEmbed = discord.Embed(
        colour = 0x28da5b,
        title = '',
        description = '''What career opportunity are you looking forward at Koders?
        > 1. Design
        > 2. Developer
        > 3. Content
        > 4. Marketing'''
    )
    apply_role = await ctx.send(embed = apply_roleEmbed)
    role_no, __tmp = await embeds.take_reaction(ctx, 4, apply_role, bot, user = user)
    if not role_no:
        await welcome.delete()
        raise Exception("'role' timed out.")
    await __tmp.delete()
    role = role_dict[role_no]
    logger.info("'role' input successful.")

    resumeEmbed = discord.Embed(
        colour = 0x28da5b,
        title = '',
        description = "Please provide your resume."
    )
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

    profileEmbed.add_field(name='Applied Role: ', value = f'{role}', inline=True)
    profileEmbed.add_field(name='Name: ', value = f'{name}', inline=True)
    profileEmbed.add_field(name='Address: ', value = f'{address}', inline=True)
    profileEmbed.add_field(name='Email Id: ', value = f'{email}', inline=True)
    profileEmbed.add_field(name='Contact Number: ', value = f'{contact}', inline=True)
    profileEmbed.add_field(name='Profession: ', value = f'{profession}', inline=True)
    profileEmbed.add_field(name='Resume', value = f'{resume}', inline=True)

    await ticket_channel.send(embed = profileEmbed)

    cursor.execute('''INSERT INTO Career
    (Role, Discord_Id, Name, Phone, Address, Mail, Profession, Resume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (role, user_id, name, contact, address, email, profession, resume))

    cursor.commit()
    cursor.close
    await ctx.send(user.mention + ", Thank You for your valuable time! We will get in touch with you as soon as possible.\nKeep Growing, Keep Koding.", delete_after = 60)
    logger.success('Data written to DB successfully')
    logger.success("'~on_react' completed successfully")


