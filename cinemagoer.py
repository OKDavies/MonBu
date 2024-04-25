from imdb import Cinemagoer

ia = Cinemagoer()

def get_movie_url(title: str) -> bool:
    """ Searches via the IMDB library whether a movie exists or not """
    movie = ia.search_movie(title) 
    movie_id = movie[0]
    movie_url = ia.get_imdbURL(movie_id)
    return movie_url