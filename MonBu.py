import os
import discord
import atexit
from dotenv import load_dotenv
from data_json.json_utils import save_data, get_json_data
from classes import Scorecard, Watchlists
import commands


load_dotenv()


def load_data():
    ratings_json = get_json_data("data_json/movies.json")
    for title, movie_data in ratings_json.items():
        scorecard.add_movie(title, movie_data)

    watchlist_json = get_json_data("data_json/watchlist.json")
    for user, wl in watchlist_json.items():
        watchlists.add_watchlist(user, wl)


scorecard = Scorecard()
watchlists = Watchlists()
load_data()


TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:   
        return
    

    if message.content.startswith('!'):
        UID = message.author.id 
        UID = str(UID)        
        msg = message.content[1:]       
        split = msg.split(' ', 1)      
        if len(split) > 1:                                
            cmd = split[0]              
            content = split[1]          
            resp = await commands.navigate(scorecard, watchlists, cmd, UID, content, client, message.channel.id)

        else:    
            cmd = split[0]
            resp = await commands.navigate(scorecard, watchlists, cmd, UID)
        await message.channel.send(resp)        
    else:
        pass          
        

atexit.register(save_data, scorecard, watchlists)

client.run(TOKEN)