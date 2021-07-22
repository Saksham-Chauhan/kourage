import discord
import csv
import pandas as pd
import datetime
from discord.ext import tasks, commands
token = '<Add token here>'  # bot token to be added here
intents = discord.Intents.all()
intents.reactions = True
intents.members = True
intents.guilds = True
class MyBot(commands.Bot):
    def __init__(self, command_prefix, self_bot, intent):
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot)

    async def on_ready(self):
        print('Logged on as', self.user)
        self.bot_send_cmd.start()
        print(self)

    @tasks.loop(hours=24)
    async def bot_send_cmd(self):
        channel = self.get_channel(854930810688110605)  #enter channel id Int format
        print(channel)
        await channel.send('!99')

    async def on_message(self,ctx):
        if ctx.author == bot.user and ctx.content=='!99':
            print("Hello")
            data = pd.DataFrame(columns=['content', 'time', 'author'])
            async for msg in ctx.channel.history(limit=1000):           # set high limit
                print(msg)
            # Trigger to fetch current date messages
                Flag = True
            # comparison of created_at sate and current date
                if(msg.created_at.strftime('%Y-%m-%d') == datetime.date.today().strftime('%Y-%m-%d')):
                    data = data.append({'content': msg.content, 'time': msg.created_at, 'author': msg.author.id}, ignore_index=True)
                else:
                    Flag = False  # if date doesn't it means that its the previous day so we break the loop

                if(Flag == False):
                    file_location = "summer_intern.csv"   # Set the string to where you want the file to be saved to
                # DataFrame creates index, which is not required while storing file in csv format
                    data.to_csv(file_location, index=False)
                #sentiment analysis
                self.sentimentAnalysis()          # in case of await function runs infinitly
            await ctx.channel.send(file=discord.File('summer-intern.png'))

    async def sentimentAnalysis(self):
        import nltk
        import pandas as pd
        import numpy as np

        data = pd.read_csv("summer_intern.csv")
        #data = data.iloc[:,1:]
        data1 = data.dropna()
        datetimeobject = lambda x: datetime.datetime.strptime(x,'%Y-%m-%d %H:%M:%S.%f').strftime('%m-%d-%Y')
        day = data1.time.apply(datetimeobject)
        data1.time = day
        print(data1.info())
        # Remove URL
        import re
        rem_url = lambda x : re.sub(r'^http\S+','',x)  
        data1_url = data1.content.apply(rem_url)

        # Remove puntuations
        remove_puntuations = lambda x: re.sub(r'[^\w\s]','',x)
        data1_url_rp = data1_url.apply(remove_puntuations)

        # Removing stopwords
        from nltk.corpus import stopwords
        stop_words = set(stopwords.words('English'))
        rem_stopwards = lambda x: ' '.join(word.lower() for word in x.split() if word not in stop_words)
        data1_url_rp_sw = data1_url_rp.apply(rem_stopwards)
        rem_extras = lambda x: None if x=='' else x
        data1_url_rp_sw_re = data1_url_rp_sw.apply(rem_extras)
        data1.content = data1_url_rp_sw_re
        data1.dropna(inplace=True)
        data1.reset_index(drop=True,inplace=True)
        from nltk.sentiment import SentimentIntensityAnalyzer
        sentiment = SentimentIntensityAnalyzer()
        import matplotlib.pyplot as plt
        sent = lambda x: sentiment.polarity_scores(x)
        sentiment_score = data1.content.apply(sent)
        score = pd.DataFrame(list(sentiment_score))
        analysis = lambda x: 'neutral' if x==0 else ('positive' if x>0 else 'negative') 
        data1['compound'] = score.compound.apply(analysis)
        df = data1.groupby(['author','compound']).size().unstack(fill_value=0)
        df1 = df.iloc[:, 0:].apply(lambda x: x.div(x.sum()).mul(100), axis=1).astype(int)
        df1.plot(kind='bar')
        plt.savefig('summer-intern.png')
        return
bot = MyBot(command_prefix='!', self_bot=False, intent=intents)
bot.run(token)
