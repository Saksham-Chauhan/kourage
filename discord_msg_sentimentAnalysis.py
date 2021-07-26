import discord
import csv
import pandas as pd
import datetime
from discord.ext import tasks, commands
token = 'ODY2NjA2OTE5OTYyOTg0NDg4.YPVAlg.dkbGE5UHFBiQmFt_qC_umxRZEU0'  # bot token to be added here
intents = discord.Intents.all()
intents.reactions = True
intents.members = True
intents.guilds = True
class MyBot(commands.Bot):

    channels = [862219851850317845]

    def __init__(self, command_prefix, self_bot, intent):
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=self_bot)

    async def on_ready(self):
        print('Logged on as', self.user)
        self.message_history.start()

    @tasks.loop(hours=24)
    async def message_history(self):
        data = pd.DataFrame(columns=['content', 'time', 'author'])
        for ch in self.channels:
            channel = self.get_channel(ch)
            print(channel)
            channel.history(limit=10)
            async for msg in channel.history(limit=1000):           # set high limit
                print(msg)
                Flag = True    # Trigger to fetch current date messages
                if(msg.created_at.strftime('%Y-%m-%d') == datetime.date.today().strftime('%Y-%m-%d')):
                    data = data.append({'content': msg.content, 'time': msg.created_at, 'author': msg.author.name}, ignore_index=True)
                else:
                    Flag = False  # if date doesn't it means that its the previous day so we break the loop
                if(Flag == False):
                    file_location = "summer_intern.csv"   
                    data.to_csv(file_location, index=False)
                self.sentimentAnalysis()          
            await channel.send(file=discord.File('summer-intern.png'))

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
        plt.xticks(range(df1.shape[0]),df1['author'],rotation=90,fontsize =3)
        plt.xlabel("Names")
        plt.ylabel("Percentage")
        plt.tight_layout()
        plt.savefig('summer-intern.png')
        return
bot = MyBot(command_prefix='!', self_bot=False, intent=intents)
bot.run(token)

