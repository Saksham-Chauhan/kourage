from datetime import datetime

import discord

header_text = "Message for the Koders"
timestamp: datetime = datetime.utcnow()
icon_url = 'https://media.discordapp.net/attachments/684768206908424226/903215466187735080/icon-01.png?width=72' \
           '&height=72 '
color = 0x76D7C4    # flagship teal color
footer_text = "Made with ❤️️ by Koders"


def morning_embed(quote, author):
    author = "<br />" + "<i>- " + author + "</i>"  # Adding proper spacing for author via HTML
    message = quote + author

    embed = discord.Embed(
        description="Good morning, folks!🔅 Let us get started to grind and shine!✨✨✨\n"
                    "*P.S. drink water and wear your socks.*",
        timestamp=timestamp,
        color=color
    )
    embed.set_author(name=header_text)
    embed.add_field(name="Before we kick off, let's have a thought", value=message, inline=False)
    embed.set_footer(text=footer_text,
                     icon_url=icon_url)

    return embed


def evening_embed():
    embed = discord.Embed(
        description="Work hard in silence and at your home being socially distant! **But do not forget to log your "
                    "work** that can make the noise of your work. So, Log your work, okay?",
        timestamp=timestamp,
        color=color
    )
    embed.set_author(name=header_text)
    embed.set_footer(text=footer_text,
                     icon_url=icon_url)

    return embed


def friday_embed():
    embed = discord.Embed(
        description="Aye hey, it is your time to take a break 😄. Communication is the key, Remember?\n"
                    "Do not forget to attend the meeting tonight. Let’s have some fun. You did great this week. "
                    "We are proud of you.\n"
                    "**#ItIsFriyay** 🥳🥳🥳.",
        timestamp=timestamp,
        color=color
    )
    embed.set_author(name=header_text)
    embed.set_footer(text=footer_text,
                     icon_url=icon_url)

    return embed
