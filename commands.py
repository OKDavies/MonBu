import random
from cinemagoer import get_movie_url
import asyncio



async def navigate(scorecard: object, watchlists: object, command: str, id=None, content=None, client=None, channel=None) -> str:
    command = command.lower()

    function_map = {
        "help": (help,),
        "ping": (ping,),
        "echo": (echo, content),
        "rate": (rate, client, channel, id, content, scorecard),
        "top": (top, content, scorecard),
        "mymovies": (mymovies, id, scorecard),
        "usermovies": (usermovies, content, scorecard),
        "add": (add, client, channel, id, content, watchlists),
        "remove": (remove, id, content, watchlists),
        "random": (random_from_watchlist, id, watchlists),
        "watchlist": (watchlist, id, content, watchlists),
        "wl": (watchlist, id, content, watchlists) 
    }

    if command in function_map:
        function_tuple = function_map[command]
        function = function_tuple[0]
        args = function_tuple[1:]
        if function == rate or function == add:
            response = await function(*args)
        else:
            response = function(*args)
    else:
        response = "I didn't recognise that command, sorry :("
    return response


def help() -> str:
    resp = """Please see below all the commands\n1. !help - Get a list of commands\n2. !ping - pong\n3. !echo - repeats the message back\n4. !rate [movie title] *[x] - Rate a movie out of 10 where x is the rating\n5. !top [x] - Get a list of top x number of movies\n6. !mymovies - Get a list of all the movies you have rated\n7. !usermovies @[user] - Get a list of all the movies a user has rated\n8. !add [movie title] - Add a movie to your watchlist\n9. !remove [movie title] - Remove a movie from your watchlist\n10. !watchlist or !wl - Return your watchlist, or tag a user to see theirs\n11. !random - Get a random movie from your watchlist\n"""
    return resp


def ping() -> str:
    return "pong"


def echo(msg: str) -> str:
    return msg


async def rate(client: object, channel: object, id: str, msg: str, scorecard: object) -> str:
    split = msg.split("*", 1)
    title = split[0].lower().strip()
    try:
        rate = int(split[1])
    except:
        return "Please make sure your rating is a number"

    if not (0 <= rate <= 10):
        return "Please make sure your rating is between 0 and 10 inclusive"
    
    hold = await confirm_movie(client, channel, id, title, "rate")
    if hold:
        scorecard.add_rating(title, id, rate)
        resp = f"<@{id}> rated {title} {rate}/10"
    else:
        resp = "Rating cancelled"
    
    return resp


def top(num: str, scorecard: object) -> str: 
    no_movies = int(num)
    top_rated_movies = scorecard.sort_movies_by_average(no_movies)
    resp = f"Top {num} rated movies:\n" 
    counter = 1                                     
    for movie in top_rated_movies:  
        resp = resp + f"{counter}. {movie.title}: Average rating: {movie.average}/10\n"
        counter = counter + 1
    return resp


def mymovies(id: str, scorecard: object) -> str: 
    if id in scorecard.movies:
        resp = "Below are all the movies you have rated:\n"
        counter = 1
        for movie in scorecard.movies:
            if id in scorecard.movies[movie].ratings:
                resp = resp + f"{counter}. {scorecard.movies[movie].title} {scorecard.movies[movie].ratings[id]}/10\n"
                counter += 1
    else:
        resp = "You haven't rated any movies yet"
    return resp


def usermovies(msg: str, scorecard: object) -> str:
    id = msg.strip("<@!>")
    if id in scorecard.movies:
        resp = f"Below are all the movies {msg} has rated:\n"
        
        counter = 1
        for movie in scorecard.movies:
            if id in scorecard.movies[movie].ratings:
                resp = resp + f"{counter}. {scorecard.movies[movie].title} {scorecard.movies[movie].ratings[id]}/10\n"
                counter += 1
    else:
        resp = f"No movies rated by <@{id}>"
    return resp


async def add(client: object, channel: object, id: str, msg: str, wl: object) -> str: 
    title = msg.lower()

    hold = await confirm_movie(client, channel, id, title, "add to your watchlist")
    if hold:
        if id in wl.watchlists:
            resp = wl.watchlists[id].add_to_watchlist(title)
        else:
            wl.add_watchlist(id, [])
            resp = wl.watchlists[id].add_to_watchlist(title)
    else:
        resp = "No movie added to your watchlist"
    return resp


def remove(id: str, msg: str, wl: object) -> str: 
    title = msg.lower()
    resp = wl.watchlists[id].remove_from_watchlist(title)
    return resp


def random_from_watchlist(id: str, wl: object) -> str: 
    try:
        movie = random.choice(wl.watchlists[id].watchlist)
    except:
        resp = "You don't have a watchlist yet, use !add [movie title] to add to your watchlist"
    else:
        resp = f"You should watch {movie}"
    return resp


def watchlist(id: str, msg: str, wl: object) -> str: 
    if msg == None:
        user = id
    else:
        user = msg.strip("<@!>")
    if user in wl.watchlists:
        counter = 1
        resp = f"<@{user}>'s watchlist\n"
        for movie in wl.watchlists[user].watchlist:
            resp = resp + f"{counter}. {movie}\n"
            counter += 1
    else:
        resp = f"<@{user}> has no watchlist"
    return resp



async def confirm_movie(client: object, channel: object, id: str, title: str, context: str):
    """ Gets a url for the user's movie, confirms with the user through waiting for a reaction
        as to whether it is the right movie"""

    movie_url = get_movie_url(title)
    confirmation_msg = await client.get_channel(channel).send(f"Is this the movie you want to {context}?\n{movie_url}")

    await confirmation_msg.add_reaction("✅")
    await confirmation_msg.add_reaction("❌")

    def check(reaction, user):
        user = str(user)
        return user == id and str(reaction.emoji) in ["✅", "❌"]

    try:
        reaction, user = await client.wait_for("reaction_add", timeout=15, check=lambda reaction, user: check(reaction, user.id))
        return str(reaction.emoji) == "✅"

    except asyncio.TimeoutError:
        """Connection timed out"""
        pass