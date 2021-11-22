from helper.embed_props import *
import discord

header_text = "Member Presence"


def get_presence_graph_embed(filename='presence_data.png'):
    embed = discord.Embed(
        description="Please remain more online during working hours if it shows less than 4 hours",
        timestamp=timestamp,
        color=color
    )
    embed.set_author(name=header_text)
    embed.set_image(filename)
    embed.set_footer(text=footer_text,
                     icon_url=icon_url)

    return embed
