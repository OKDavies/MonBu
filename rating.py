import json
import string
from imdb import Cinemagoer

rating_file = 'ratings.json'
ia = Cinemagoer()








# Gets the movies of either a specified user <@user_id> or the user executing the command

def user_movies(UID):           # Called by the bot commands !mymovies or !usermovies <@user>

    # print(UID)

    user_movies = get_user_movies(UID)          # Gets all the movies rated by the user (UID) specified in the command or if not specified 
                                                # then from the user executing the command. This is handled by the call to the function.

    if user_movies:         # Checks to see if there are movies rated by the user (If there are then user_movies will not be empty)

        response = f"Movies rated by user <@{UID}>:\n"      # Start the format for the response

        counter = 1                                         # Counts for the list numbering

        ratings = load_ratings()        # Load existing ratings from JSON file

        for movie in user_movies:       # Loop through the user rated movies and create response

            movie_rating = ratings[movie]['ratings'][UID]       

            response += f"{counter}. {movie}: {movie_rating}/10\n"

            counter += 1

    else:

        response = f"No movies have been rated by user <@{UID}>."       # If no movies rated by requested user then return this statment
    
    return response












# Write the ratings to the json file

def save_ratings(ratings):          # Called internally by add_rating

    with open(rating_file, 'w') as file:

        json.dump(ratings, file, indent=4)



# Gets all movies rated by a specific user

def get_user_movies(user_id):       # Called internally by user_movies

    
    ratings = load_ratings()        # Load existing ratings from JSON file

    str_user_id = str(user_id)      # Convert the user ID to a string

    user_movies = []

    for movie, data in ratings.items():

        if str_user_id in data['ratings']:

            user_movies.append(movie)

    return user_movies

