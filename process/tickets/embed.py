from helper.embed_props import *
import discord


def get_open_issues_embed(data):
    header_text = "**Open Issues**"
    embed = discord.Embed(
        description="**Please clear these issues asap** \n" + data,
        timestamp=timestamp,
        color=color
    )
    embed.set_author(name=header_text)
    embed.set_footer(text=footer_text,
                     icon_url=icon_url)

    return embed


def get_resolved_issues_embed(data):
    header_text = "**Resolved Issues**"
    embed = discord.Embed(
        description="**Dear mentors, Please close these issues asap** \n" + data,
        timestamp=timestamp,
        color=color
    )
    embed.set_author(name=header_text)
    embed.set_footer(text=footer_text,
                     icon_url=icon_url)

    return embed
