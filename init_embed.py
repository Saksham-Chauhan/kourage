import os
import embeds
import discord
from discord.ext.tasks import loop
from discord.ext import commands

bot = commands.Bot(command_prefix="~")
#####################################
###         EDITABLES           #####
#####################################
channel_ids = [868909086803132466, 868908609591975967, 868909118147166229]
rules_channel = 866578020713103360


async def init_rules(channel):
    embed = discord.Embed(title="**Welcome Aboard!**",
                          description="""HELLO! THANK YOU FOR CHOOSING KODERS.

            At Koders, we adhere to certain set of **rules**.
            > 
            > 1. Welcome to our Private Discord server! It would take a few moments for you to let us know your reason of joining.
            > 
            > 2. Once it's done,we would happily assist you to get the most from our side.
            > 
            > 3. We would like you to go through the ***#GUIDELINES*** to have a better insight of our functioning.
            > 
            > 4. We value you! Rest assured, all your personal details will be safe with us.
            > 
            > 5. In case of any doubts, our Management team is always there to help you out.
            > 
            > 6. Do maintain the decorum of the server. We would really appreciate that!
            > 

            To get started,
            Please react on this message to be a part of our journey!"""
                          , colour=0x11806a)

    embed.set_thumbnail(
        url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    embed.set_footer(text="Welcome to Koders ❤️️")
    send = await channel.send(embed=embed)
    await send.add_reaction('⬆️')

    return


async def init_onboarding(channels):
    embed = discord.Embed(title="Welcome to **KODERS**!",
                          description="""
            We're glad to have you on board with us!
            **VISION | KREATE | INSPIRE**

            Koders katers to all your software needs with the touch of Koding.
            We welcome you to a community full of vibrance and fruition.
            To know more about us, visit [Koders](@https://koders.in/).

            We would like to know more about you, please ⬆️ react on the message to generate a ticket for your project!

            For any queries, feel free to reach out to us at:
            > 
            > support@koder.in
            > 
            Or call us at:
            > 
            > +91 7008493497
            > +91 7017799756

            """
                          , colour=0x11806a)

    embed.set_thumbnail(
        url="https://media.discordapp.net/attachments/700257704723087360/819643015470514236/SYM_TEAL.png?width=455&height=447")
    embed.set_footer(text="Welcome to Koders ❤️️")
    for channel in channels:
        send = await channel.send(embed=embed)
        await send.add_reaction('⬆️')
    return


@bot.event
async def on_ready():
    await init_rules(bot.get_channel(rules_channel))
    channels = list()

    for i in channel_ids:
        channels.append(bot.get_channel(i))

    await init_onboarding(channels)


bot.run(os.environ.get("TOKEN"))
