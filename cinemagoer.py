from imdb import Cinemagoer

ia = Cinemagoer()

def is_valid_movie(title: str) -> bool:
    """ Searches via the IMDB library whether a movie exists or not """
    movie = ia.search_movie(title) 
    movie = movie[0]["title"].lower().strip()
    title = title.lower().strip()
    return movie == title