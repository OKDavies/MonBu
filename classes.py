import string



class Scorecard():
    """ This class will store all the data for each movie that has ben rated by a user.
        Future development of this class and the susequent Movie class would be to 
        incorporate more information about the movies such as, description, run length,
        actors, etc. """
    

    def __init__(self) -> None:
        self.movies: dict[str, object]= {}


    def add_movie(self, title: str, data: dict) -> None:
        self.movies[title] = Movie(title, data)


    def add_rating(self, title: str, user: str, rate: int) -> None:
        """ Either adds a rating to an existing movie in the object or 
            creates a new entry for the movie then adds the rating """
        title = string.capwords(title)
        if title in self.movies:
            self.movies[title].add_rating(user, rate)
        else:
            self.add_movie(title, {"ratings":{user: rate}})


    def sort_movies_by_average(self, num: int) -> list:
        sorted_movies = sorted(self.movies.values(), key=lambda movie: movie.average, reverse=True)
        return sorted_movies[:num]


class Movie():


    def __init__(self, title: str, data: dict) -> None:
        self.title = title
        self.ratings = data["ratings"]
        self.average = self.average_rating()
        #self.description = data["description"]
        #self.run_length = data["run_length"]

    
    def add_rating(self, user: str, rating: int) -> None:
        if user in self.ratings:
            self.ratings.pop(user)
            self.ratings[user] = rating
        else:
            self.ratings[user] = rating


    def average_rating(self) -> None:
        total_rating = sum(self.ratings.values())
        return total_rating / len(self.ratings)



class Watchlists():
    """ This class stores all the watchlist information for each user.
        Future development would see this class handle an ordering system
        so the user can rank their priority for what they want to watch. 
        Possibly adding a feature to track the date and giving reminders once x
        weks have passed with a movie on their watchlist """
    

    def __init__(self) -> None:
        self.watchlists: dict[str, object] = {}


    def add_watchlist(self, user: str, wl: list) -> None:
        self.watchlists[user] = Watchlist(wl)



class Watchlist():


    def __init__(self, wl: list) -> None:
        self.watchlist: list[str] = wl

    
    def add_to_watchlist(self, title: str) -> str:
        resp = "Something went wrong :("
        title = string.capwords(title)
        if title in self.watchlist:
            resp = "Movie is already in your watchlist"
        else: 
            self.watchlist.append(title)
            resp = f"{title} has been added to your watchlist"
        return resp
    

    def remove_from_watchlist(self, title: str) -> str:
        title = string.capwords(title)
        if title in self.watchlist:
            self.watchlist.remove(title)
            resp = f"{title} was removed from your watchlist"
        else:
            resp = f"{title} could not be found in your watchlist"
        return resp