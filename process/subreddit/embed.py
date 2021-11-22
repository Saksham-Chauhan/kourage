from helper.embed_props import *
import discord


def get_subreddit_meme_embed(title, url):
    header_text = title
    embed = discord.Embed(
        timestamp=timestamp,
        color=color
    )
    embed.set_author(name=header_text)
    embed.set_image(url)
    embed.set_footer(text=footer_text,
                     icon_url=icon_url)

    return embed
