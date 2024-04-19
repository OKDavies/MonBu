import random
from classes import InvalidMovie


def navigate(command: str, id=None, content=None) -> str:
    command = command.lower()

    function_map = {
        #"test": (test,),
        "help": (help,),
        "ping": (ping,),
        "echo": (echo, content),
        "rate": (rate, id, content),
        "top": (top, content),
        "mymovies": (mymovies, id),
        "usermovies": (usermovies, content),
        "add": (add,id, content),
        "remove": (remove, id, content),
        "random": (random_from_watchlist, id),
        "watchlist": (watchlist, id, content),
        "wl": (watchlist, id, content) 
    }

    if command in function_map:
        function_tuple = function_map[command]
        function = function_tuple[0]
        args = function_tuple[1:]
        response = function(*args)
    else:
        response = "I didn't recognise that command, sorry :("
    return response


#def test():
    """ !test 
        Can ignore, used to test things"""
    #for title, data in scorecard.movies.items():
        #print(title)
        #print(scorecard.movies[title])
        #print(scorecard.movies[title].ratings)
    #return "Testing"


def help() -> str:
    """ !help
        Used to give the user all the commands 
        and how to use them """
    resp = """Please see below all the commands\n1. !help - Get a list of commands\n2. !ping - pong\n3. !echo - repeats the message back\n4. !rate [movie title] *[x] - Rate a movie out of 10 where x is the rating\n5. !top [x] - Get a list of top x number of movies\n6. !mymovies - Get a list of all the movies you have rated\n7. !usermovies @[user] - Get a list of all the movies a user has rated\n8. !add [movie title] - Add a movie to your watchlist\n9. !remove [movie title] - Remove a movie from your watchlist\n10. !watchlist or !wl - Return your watchlist, or tag a user to see theirs\n11. !random - Get a random movie from your watchlist\n"""
    return resp

def ping() -> str:
    """ !ping
        Used to test the bot is active quickly """
    return "pong"


def echo(msg: str) -> str:
    """ !echo {content}           
        Returns the text written in the 
        command as a message from the bot """ 
    return msg


def rate(id: str, msg: str) -> str:
    """ !rate [movie title] *[x]          
        Allows the message author to rate a movie x /10 """
    split = msg.split("*", 1)
    title = split[0].lower()
    try:
        rate = int(split[1])
    except:
        resp = "Please make sure your rating is a number"
    else:
            if 0 <= rate < 10:
                try:
                    scorecard.add_rating(title, id, rate)
                except InvalidMovie:
                    resp = "This movie could not be found, please check the spelling and try again"
                except:
                    resp = "Something went wrong :("
                else:
                    resp = f"<@{id}> rated {title} {rate}/10"
                
            else:
                resp = "Please make sure your rating is between 0 and 10 inclusive"
    return resp


def top(num: str) -> str: 
    """ !top [x]          
        Where x is an integer, returns the top 
        rated x number of movies """
    no_movies = int(num)
    top_rated_movies = scorecard.sort_movies_by_average(no_movies)
    print(top_rated_movies)
    resp = f"Top {num} rated movies:\n" 
    counter = 1                                     
    for movie in top_rated_movies:  
        resp = resp + f"{counter}. {movie.title}: Average rating: {movie.average}/10\n"
        counter = counter + 1
    return resp


def mymovies(id: str) -> str: 
    """ !mymovies         
        Returns movies rated by the message author
        executing the command """
    resp = "Below are all the movies you have rated:\n"
    counter = 1
    for movie in scorecard.movies:
        print(movie)
        if id in scorecard.movies[movie].ratings:
            print("here")
            resp = resp + f"{counter}. {scorecard.movies[movie].title} {scorecard.movies[movie].ratings[id]}/10\n"
            counter += 1
    return resp


def usermovies(msg: str) -> str:
    """ !usermovies <@user>           
        Returns the movies rated by the specified user """
    resp = f"Below are all the movies {msg} has rated:\n"
    id = msg.strip("<@!>")
    counter = 1
    for movie in scorecard.movies:
        print(movie)
        if id in scorecard.movies[movie].ratings:
            resp = resp + f"{counter}. {scorecard.movies[movie].title} {scorecard.movies[movie].ratings[id]}/10\n"
            counter += 1
    return resp


def add(id: str, msg: str) -> str: 
    """ !add [movie title]                
        Adds a movie to message author's watchlist """
    title = msg.lower()
    if id in wl.watchlists:
        resp = wl.watchlists[id].add_to_watchlist(title)
    else:
        wl.add_watchlist(id, [])
        resp = wl.watchlists[id].add_to_watchlist(title)
    return resp


def remove(id: str, msg: str) -> str: 
    """ !remove [title]           
        Removes movie from message author's watchlist """
    title = msg
    if title in wl.watchlists[id].watchlist:
        wl.watchlists[id].watchlist.remove(title)
        resp = f"{title} removed from your watchlist."
    else:
        resp = f"{title} was not found in your watchlist"
    return resp


def random_from_watchlist(id: str) -> str: 
    """ !random                   
        Returns a random movie from message author's watchlist """
    print(wl.watchlists[id].watchlist)
    try:
        movie = random.choice(wl.watchlists[id].watchlist)
    except:
        resp = "You don't have a watchlist yet, use !add [movie title] to add to your watchlist"
    else:
        resp = f"You should watch {movie}"
    return resp


def watchlist(id: str, msg: str) -> str: 
    """ !watchlist or !wl                   
        Gets message author's or specified user's
        watchlist. """
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
