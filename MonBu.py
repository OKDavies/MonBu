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
    # Ignore messages sent by the bot itself
    if message.author == client.user:   
        return
    

    # If message is a command (starts with a "!") break up the command and content and send to commands.py script 'input'
    if message.content.startswith('!'):
        UID = message.author.id 
        UID = str(UID)        
        msg = message.content[1:]       
        split = msg.split(' ', 1)      
        # Checks whether the command has content or is just a single word command
        if len(split) > 1:                                
            cmd = split[0]              
            content = split[1]          
            resp = commands.navigate(scorecard, watchlists, cmd, UID, content)

        else:    
            cmd = split[0]
            resp = commands.navigate(scorecard, watchlists, cmd, UID)
        # print(UID)
        # print(resp)
        # Send a message with the response from the executed command
        await message.channel.send(resp)        
    else:
        pass            # Ignore any messages that don't start with the command prefix
        

atexit.register(save_data, scorecard, watchlists)

client.run(TOKEN)