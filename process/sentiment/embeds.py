from datetime import datetime

import discord

header_text = "Member Sentiments"
timestamp: datetime = datetime.utcnow()
icon_url = 'https://media.discordapp.net/attachments/684768206908424226/903215466187735080/icon-01.png?width=72' \
           '&height=72 '
color = 0x76D7C4    # flagship teal color
footer_text = "Made with ❤️️ by Koders"


def get_sentiment_graph_embed(filename='sentiment_data.png'):
    embed = discord.Embed(
        description="Please remain more kind and humble during working hours if it shows more than 50% negative",
        timestamp=timestamp,
        color=color
    )
    embed.set_author(name=header_text)
    embed.set_image(filename)
    embed.set_footer(text=footer_text,
                     icon_url=icon_url)

    return embed
