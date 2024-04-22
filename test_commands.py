import unittest
from classes import Scorecard, Watchlists
from commands import rate, top, mymovies, usermovies, add, remove, random_from_watchlist, watchlist

"""        "rate": (rate, id, content),
        "top": (top, content),
        "mymovies": (mymovies, id),
        "usermovies": (usermovies, content),
        "add": (add,id, content),
        "remove": (remove, id, content),
        "random": (random_from_watchlist, id),
        "watchlist": (watchlist, id, content),
        "wl": (watchlist, id, content)"""

scorecard = Scorecard()
scorecard.add_movie("Movie 1", {"ratings": {"user1": 8, "user2": 7}, "average": 7.5})
scorecard.add_movie("Movie 2", {"ratings": {"user1": 6, "user3": 9}, "average": 7.5})
scorecard.add_movie("Movie 3", {"ratings": {"user2": 9}, "average": 9.0})
scorecard.add_movie("Test", {"title": "Test", "ratings": {"1234": 3}, "average": 3})




def test_rate_an_existing_movie():
    # Update existing user's rating
    assert rate("1234", "test *4", scorecard) == "<@1234> rated test 4/10"
    assert scorecard.movies["Test"].ratings["1234"] == 4

    #Adding a new user to exisiting movie ratings
    assert rate("0987", "test *6", scorecard) == "<@0987> rated test 6/10"
    assert scorecard.movies["Test"].ratings["0987"] == 6


def test_rating_not_an_integer():
    assert rate("1234", "test *abc", scorecard) == "Please make sure your rating is a number"


def test_movie_is_valid():
    assert rate("1234", "definitely not a movie, *6", scorecard) == "This movie could not be found, please check the spelling and try again"


def test_rating_is_in_bounds():
    assert rate("1234", "test *11", scorecard) == "Please make sure your rating is between 0 and 10 inclusive"
    assert rate("1234", "test *-1", scorecard) == "Please make sure your rating is between 0 and 10 inclusive"




def test_top_movies():
    result = top("2", scorecard)
    assert "Top 2 rated movies:" in result
    assert "1. Movie 3: Average rating: 9.0/10" in result
    assert "2. Movie 1: Average rating: 7.5/10" in result



def test_mymovies():
    result = mymovies("user1", scorecard)
    assert "Below are all the movies you have rated:" in result
    assert "1. Movie 1 8/10" in result
    assert "2. Movie 2 6/10" in result




def test_usermovies():
    result = usermovies("<@user2>", scorecard)
    assert "Below are all the movies <@user2> has rated:" in result
    assert "1. Movie 1 7/10" in result
    assert "2. Movie 3 9/10" in result





def test_add():
    watchlists = Watchlists()
    watchlists.add_watchlist("user1", ["movie1", "movie2"])
    result = add("user1", "Shrek", watchlists)
    assert result == "Shrek has been added to your watchlist"
    result = add("user2", "Another New Movie", watchlists)
    assert result == "Movie could not be found please check the spelling and try again."
    result = add("user2", "Shrek", watchlists)
    assert result == "Shrek has been added to your watchlist"



def test_remove():
    watchlists = Watchlists()
    watchlists.add_watchlist("user1", ["movie1", "movie2"])
    result = remove("user1", "movie1", watchlists)
    assert result == "movie1 removed from your watchlist."
    result = remove("user1", "movie3", watchlists)
    assert result == "movie3 was not found in your watchlist"



def test_random_from_watchlist():
    watchlists = Watchlists()
    watchlists.add_watchlist("user1", ["movie1", "movie2"])
    result = random_from_watchlist("user1", watchlists)
    assert result in ["You should watch movie1", "You should watch movie2"]



def test_watchlist():
    watchlists = Watchlists()
    watchlists.add_watchlist("user1", ["movie1", "movie2"])
    result = watchlist("user1", None, watchlists)
    assert "<@user1>'s watchlist" in result
    assert "1. movie1" in result
    assert "2. movie2" in result



if __name__ == '__main__':
    unittest.main()