from discord.ext.commands import Bot
from discord.ext import tasks
from discord import Member
import discord
import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
token = '<Add token here>'  # bot token to be added here

intents = discord.Intents.all()
intents.members= True
bot = Bot(command_prefix='!', intents = intents)
data = {}   # creating a dict to stpre info in the following format {user:{total_time:'',start_time:''}}

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))
    load_dictionary_koders.start()    #starts the task event

@tasks.loop(hours=24)
async def load_dictionary_koders():
    guild = bot.get_guild(854930810688110602) # enter server guil in Int format
    #graph plotting from previous days data
    if len(data)!=0:
        ids = data.keys()
        totaltime = []
        for x in ids:
            totaltime.append(int(data[x]['total_time'].total_seconds()))
        plt.bar(ids,totaltime)
        plt.show()
    # runs after every 24 hours
    # restoring the dictionary, setting all values to 0
    # in case of online status when the task runs, start_time is set to current time
    for member in guild.members:
        for role in guild.roles:
            if role.name=="Koders":
                if member.status == discord.Status.online:   #to check user status when the task runs
                    data[member.name] = {"total_time": datetime.timedelta(0), 'start_time':datetime.datetime.now()}
                else:
                    data[member.name]= {'total_time':datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0), 'start_time':0}
#runs incase of status change of any member
@bot.event
async def on_member_update(usr_before, usr_after):
    print(usr_before.status)
    print(usr_after.name)
    #if start_time = 0 that means the user was previously offline and now online 
    if(data[usr_before.name]['start_time'] == 0):
        data[usr_before.name]['start_time'] = datetime.datetime.now()
    # total_time is calculate by  substracting the current time with start_time when the user goes offline
    # start_time is the set to 0
    else:
        data[usr_before.name]['total_time'] += (datetime.datetime.now()-data[usr_before.name]['start_time'])
        data[usr_before.name]['start_time'] = 0
        print(data[usr_before.name]['total_time'])
    
bot.run(token)
