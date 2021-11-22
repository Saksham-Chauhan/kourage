from helper.embed_props import *
import discord

header_text = "Member spent time"


def get_spent_graph_embed(data, filename='spent_time_data.png'):
    embed = discord.Embed(
        description="**Please log more hours if it shows less than 4 hours** \n" + data,
        timestamp=timestamp,
        color=color
    )
    embed.set_author(name=header_text)
    embed.set_image(filename)
    embed.set_footer(text=footer_text,
                     icon_url=icon_url)

    return embed
