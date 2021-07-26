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

##########################################333
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

    #TODO: Create function to handle repition of code
    client_name_embed=discord.Embed(title="",description="What's your good name?",colour=0x11806a)
    client=await ctx.send(embed=client_name_embed)
    client_name = await embeds.ctx_input(ctx, bot, client, user = user, type = "name")
    if not client_name:
        await welcome.delete()
        raise Exception("'client_name' timed out.")
    logger.info("'client_name' input successful.")
 
    address_embed=discord.Embed(title="",description="Please enter your address.",colour=0x11806a)
    address=await ctx.send(embed=address_embed,delete_after=60)
    client_address = await embeds.ctx_input(ctx, bot, address, user = user)
    if not client_address:
        await welcome.delete()
        raise Exception("'client_address' timed out.")
    logger.info("'client_address' input successful.")

    email_embed=discord.Embed(title="",description="Please provide your email-id.",colour=0x11806a)
    email=await ctx.send(embed=email_embed,delete_after=60)
    client_email = await embeds.ctx_input(ctx, bot, email, user = user, type = "email")
    if not client_email:
        await welcome.delete()
        raise Exception("'client_email' timed out.")
    logger.info("'client_email' input successful.")

    phone_embed=discord.Embed(title="",description="Please enter your contact number.",colour=0x11806a)
    phone=await ctx.send(embed=phone_embed,delete_after=60)
    client_phone = await embeds.ctx_input(ctx, bot, phone, user = user, type = "phone")
    if not client_phone:
        await welcome.delete()
        raise Exception("'client_phone' timed out.")
    logger.info("'client_phone' input successful.")

    org_name_embed=discord.Embed(title="",description="Please enter your Organisation's name.",colour=0x11806a)
    org_name_sent = await ctx.send(embed=org_name_embed,delete_after=60)
    org_name = await embeds.ctx_input(ctx, bot, org_name_sent, user = user)
    if not org_name:
        await welcome.delete()
        raise Exception("'org_name' timed out.")
    logger.info("'org_name' input successful.")
    
    project_details_embed=discord.Embed(title="",description="How can we assist you? Enter the project details so that our management team can get in touch with you.",colour=0x11806a)
    project=await ctx.send(embed=project_details_embed,delete_after=60)
    project_details = await embeds.ctx_input(ctx, bot, project, user = user)
    if not project_details:
        await welcome.delete()
        raise Exception("'project_details' timed out.")
    logger.info("'project_details' input successful.")

    event_id = datetime.datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
    unique_id = event_id[48:].upper()

    await welcome.delete()

    await ctx.send('Thank you for your valuable time! We will get in touch with you as soon as possible.', delete_after = 60)
    # For the sake of record, we can save the ticket details on a ticket channel.
    sendEmbed=discord.Embed(
            title="NEW PROJECT REQUEST\n",
            description="",
            colour=0x11806a
            )
    sendEmbed.set_author(name = f'Ticket raised by : {user.name}', icon_url = f'{user.avatar_url}')
    sendEmbed.add_field(name='Ticked Id: ', value = str(unique_id)+"\n\n\n", inline=False)
    sendEmbed.add_field(name='Client Name: ', value = str(client_name)+"\n\n", inline=False)
    sendEmbed.add_field(name='Client contact details: ', value = "Address: "+str(client_address)+"\nEmail: "+str(client_email)+"\nPhone no: "+str(client_phone)+"\n\n\n", inline=False)
    sendEmbed.add_field(name='Organisation: ', value =str(org_name)+"\n\n\n", inline=False)
    sendEmbed.add_field(name='Project Details: ', value =str(project_details)+"\n\n\n", inline=False)

    message = await ticket_channel.send(embed = sendEmbed)

    guild = ticket_channel.guild
    category = None
    for i in guild.categories:
        if i.name == "Client":
            category = i
            break

    if not category:
        category = await guild.create_category("Client")

    role_name = 'client_' + str(unique_id)
    role = await guild.create_role(name = role_name)
    await user.add_roles(role)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        discord.utils.get(guild.roles, name = 'client_' + str(unique_id)): discord.PermissionOverwrite(read_messages=True),
        discord.utils.get(guild.roles, name = 'management'): discord.PermissionOverwrite(read_messages=True),
        guild.me: discord.PermissionOverwrite(read_messages=True)
        }

    new_client_channel = await guild.create_text_channel(role_name, overwrites=overwrites, category = category)
    await new_client_channel.send(embed = sendEmbed)
    await new_client_channel.send("Please wait a while. The management team will get back to you soon.")
    logger.success('~on_react executed successfully.')

