import datetime
from uuid import uuid4
import discord
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
        description="You're almost there!\nPlease provide the following details.",
        colour=0x11806a
    )
    welcome_embed.set_thumbnail(
        url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    welcome_embed.set_footer(text="Welcome to Koders ❤️️")
    welcome_embed.set_author(name=f'Bot initialized for  {user.name}', icon_url=f'{user.avatar_url}')
    welcome_embed.timestamp = datetime.datetime.utcnow()
    welcome = await ctx.send(embed=welcome_embed)

    partner_name_embed = discord.Embed(title="", description="What's your good name?", colour=0x11806a)
    partner = await ctx.send(embed=partner_name_embed)
    partner_name = await embeds.ctx_input(ctx, bot, partner, user=user, type="name")
    if not partner_name:
        await welcome.delete()
        raise Exception("'partner_name' timed out.")
    logger.info("'partner_name' input successful.")

    address_embed = discord.Embed(title="", description="Please enter your address", colour=0x11806a)
    address = await ctx.send(embed=address_embed)
    partner_address = await embeds.ctx_input(ctx, bot, address, user=user)
    if not partner_address:
        await welcome.delete()
        raise Exception("'partner_address' timed out.")
    logger.info("'partner_address' input successful.")

    email_embed = discord.Embed(title="", description="Please provide your email-id", colour=0x11806a)
    email = await ctx.send(embed=email_embed)
    partner_email = await embeds.ctx_input(ctx, bot, email, user=user, type="email")
    if not partner_email:
        await welcome.delete()
        raise Exception("'partner_email' timed out.")
    logger.info("'partner_email' input successful.")

    phone_embed = discord.Embed(title="", description="Please enter your contact number.", colour=0x11806a)
    phone = await ctx.send(embed=phone_embed)
    partner_phone = await embeds.ctx_input(ctx, bot, phone, user=user, type="phone")
    if not partner_phone:
        await welcome.delete()
        raise Exception("'partner_phone' timed out.")
    logger.info("'partner_phone' input successful.")

    organisation_name_embed = discord.Embed(title="", description="Please enter your Organisation's Name?",
                                            colour=0x11806a)
    organisation = await ctx.send(embed=organisation_name_embed)
    organisation_name = await embeds.ctx_input(ctx, bot, organisation, user=user)
    if not organisation_name:
        await welcome.delete()
        raise Exception("'organisation_name' timed out.")
    logger.info("'organisation_name' input successful.")

    reason_embed = discord.Embed(title="", description="Please specify why do you want to be partners with us.",
                                 colour=0x11806a)
    reason = await ctx.send(embed=reason_embed)
    reason = await embeds.ctx_input(ctx, bot, reason, user=user)
    if not reason:
        await welcome.delete()
        raise Exception("'reason' timed out.")
    logger.info("'reason' input successful.")

    event_id = datetime.datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
    unique_id = event_id[48:].upper()

    await welcome.delete()

    await ctx.send(
        user.mention + ", Thank You for your valuable time! We will get in touch with you as soon as possible.\nKoders is looking forward to a good Partnership.",
        delete_after=60)

    thankyou_embed = discord.Embed(
        title="Thank your ticket is genrated successfully",
        description="We will get back to you very soon",
        color=0x11806a
    )

    reviewEmbed = discord.Embed(title="", description="", color=0x11806a)
    reviewEmbed.set_author(name=f'Ticket raised by : {user.name}', icon_url=f'{user.avatar_url}')
    reviewEmbed.add_field(name='Ticked Id: ', value=str(unique_id) + "\n\n\n", inline=False)
    reviewEmbed.add_field(name='Partner Name:', value=str(partner_name) + "\n\n", inline=False)
    reviewEmbed.add_field(name='Partner contact details:', value="Address: " + str(partner_address) + "\nEmail: " + str(
        partner_email) + "\nPhone no: " + str(partner_phone) + "\n\n\n", inline=False)
    reviewEmbed.add_field(name='Organisation Name:', value=str(organisation_name) + "\n\n\n", inline=False)
    reviewEmbed.add_field(name='Why they want to join:', value=str(reason) + "\n\n\n", inline=False)

    message = await ticket_channel.send(embed=reviewEmbed)

    guild = ticket_channel.guild
    category = None
    for i in guild.categories:
        if i.name == "Partner":
            category = i
            break

    if not category:
        category = await guild.create_category("Partner")

    role_name = 'partner_' + str(unique_id)
    role = await guild.create_role(name=role_name)
    await user.add_roles(role)

    # Overwrites permissions to only let the management, new user and the admin(s)
    # to view and message in the channel.
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        discord.utils.get(guild.roles, name='partner_' + str(unique_id)): discord.PermissionOverwrite(
            read_messages=True),
        discord.utils.get(guild.roles, name='management'): discord.PermissionOverwrite(read_messages=True),
        guild.me: discord.PermissionOverwrite(read_messages=True)
    }

    new_partner_channel = await guild.create_text_channel(role_name, overwrites=overwrites, category=category)
    await new_partner_channel.send(embed=reviewEmbed)
    await new_partner_channel.send("Please wait a while. The management team will get back to you soon.")

    logger.success("'~on_react' executed successfully.")
