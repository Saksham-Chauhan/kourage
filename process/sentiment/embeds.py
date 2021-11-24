from helper.embed_props import *
import discord

header_text = "Member Sentiments"


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
