import os
import discord
import aioschedule

from dotenv import load_dotenv
load_dotenv()

CHANNEL_ID = 938461049617809438
TOKEN =  "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"
TIME = "03:00"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    aioschedule.every().day.at(TIME).do(message)
    while True:
        await aioschedule.run_pending()


async def message():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send("""[Previous Experience] : Web designing and development, desktop apps, custom discord bots, modules and toolbots, GUIs and toolbots, backend scripts, NFT toolbots, mobile apps
[Availability]: FRONTEND DEV TEAM
[Programming languages]: React, Electron, Javascript, HTML, CSS, Node, Express, MongoDb, React Native, Python, Docker, Hasura, Graphql, Flutter, Vue, Next, Tailwind
[Plenty Of Experience Just Ask For Past Projects]
[Previous Groups I Developed For]: Xenox labs, Platinum AIO, Vyperr scripts, GG, Zeus, Amenity, Genesis, Squared, Astro, Divine, Hawa, Nuclear, AIOWorld, Machina, UC-Toolbot, Gotham, Crystyl, Jupiter, PopBot, Argon AIO, Junodraw, Arc AIO, Epon NFT, KyroTools, Epon NFT, Metamint, Bolt AIO
[Availability]: 35-40 Hours Per week""")

try:
    client.run(os.getenv(TOKEN))
except Exception as error:
    print("Error running Discord selfbot:", error)

