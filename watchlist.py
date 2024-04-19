import json
import random




# Adds a movie to a user's watchlist

def add_to_watchlist(movie_title, user_id):                 # Called by the bot command !add

    fix = str(user_id)                      # ID needs to be a string to find key in dictionary

    fix.strip()                         # Remove any possible whitespace

    full_watchlist = load_watchlist()                   # Get the full dictionary from the json file

    valid_movie = "is_valid_movie(movie_title) "           # Check the movie exists on IMDb

    if valid_movie == False:                     # If the movie cannot be found return an error

        print("here")

        resp = "No movie could be found by that title, please check your spelling and try again."

    else:

        if fix in full_watchlist:                     # If the user has a dictionary nested then add to it

            if valid_movie in full_watchlist[fix]:           # If the movie already exists on the watchlist return an error

                resp = "This movie is already on your watchlist, consider watching it?"

            else:       

                position = len(full_watchlist[fix]) + 1              # Set the position as one more than exist in the users dictionary

                full_watchlist[fix][valid_movie] = position          # Add a key and value to the dictionary

                save_watchlist(full_watchlist)               # Save the new dictionary to json

                msg = f'<@{user_id}> added {position}. {valid_movie} to their watchlist.'            # Format a completion message

                resp = msg

        else:                    # User has not added a movie to their watchlist before so add a new nest to the json dictionary

            position = 1                 # Set the position for the new entry

            full_watchlist = {                      # Make and add a new nested dictionary to the json dictionary
                fix: {
                    valid_movie: position
                    }
            }

            save_watchlist(full_watchlist)      # Save to the json file

            msg = f'<@{user_id}> added {position}. {valid_movie} to their watchlist.'       # Format a completion message

            resp = msg

    return resp




# Creates a message response to show a users watchlist

def show_watchlist(user_id):                # Calle by the bot command !watchlist or !wl

    user_watchlist = get_user_watchlist(user_id)                # Get the full watchlist of a user

    if user_watchlist:         # Checks to see if there is a watchlist for the user, if yes format the response

        response = f"<@{user_id}> watchlist:\n"      # Start the format for the response

        counter = 1

        for movie in user_watchlist:       # Loop through the user rated movies and create response  


            response += f"{counter}. {movie}\n"

            counter += 1

    else:

        response = f"No movies on the watchlist for <@{user_id}>."       # If no movies on user watchlist then return this statment
    
    return response




# Starts the removal process by finding the movie to be removed from the users watchlist and deleting it

def remove_from_watchlist(user_id, position):                   # Called by the bot command !remove

    user_watchlist = get_user_watchlist(user_id)                # Gets the user's watchlist

    for x in user_watchlist.copy():                     # Uses a copy of the dict so it can be edited during the loop

        int(position)                   # Make sure variable is an int, the same as it is stored in the dictionary

        int(user_watchlist[x])          # Make sure variable is an int, the same as it is stored in the dictionary

        if position == user_watchlist[x]:               # When the input position to be removed is found...

            user_watchlist.pop(x)                       # remove the selection

    counter = 1

    for x in user_watchlist:                    # Re-order the movies in the watchlist to start from 1

        user_watchlist[x] = counter

        counter += 1

    new_watchlist = make_new_watchlist(user_watchlist, user_id)         # New watchlist made to be sent to json

    save_watchlist(new_watchlist)                           # Save the full dictionary to json

    return "removie"





# 

def get_random_movie(user_id):

    user_watchlist = get_user_watchlist(user_id)

    list1 = []
    
    counter = 0

    for movie in user_watchlist:

        list1.append(movie)

    selection = random.choice(list1)

    response = f"You should try watching: {selection}."

    return response



#   Creates the new watchlist json dictionary to be saved, includes other user's watchlists

def make_new_watchlist(updated_order, user_id):         # Called internally by remove_from_watchlist

    old_order = load_watchlist()                        # Load the old watchlist to be edited

    user_id = str(user_id)                              # Needs to be string for the key to be found in dict

    old_order.pop(user_id)                              # Remove old ordered watchlist for that user

    old_order.update({user_id: updated_order})          # Add back in the edited watchlist for the user

    return old_order
    



# Load contents of the watchlist file

def load_watchlist():                 # Called internally by add_to_watchlist, make_new_watchlist, and get_user_watchlist

    try:

        with open('watchlist.json', 'r') as file:        # If successful, dictionary from file will be pulled 

            watchlist = json.load(file)

    except FileNotFoundError:

        watchlist = {}        # If unsuccessful empty dictionary exists 

    # print(watchlist)

    return watchlist



# Write the watchlist to the json file

def save_watchlist(data):          # Called internally by add_to_watchlist, and remove_from_watchlist

    with open('watchlist.json', 'w') as file:

        json.dump(data, file, indent=4)




# Gets the watchlist of a specific user and returns as a dictionary

def get_user_watchlist(user_id):            # Called internally by remove_from_watchlist

    watchlist = load_watchlist()        # Load existing ratings from JSON file

    str_user_id = str(user_id)      # Convert the user ID to a string

    if str_user_id in watchlist:        # Checks the user has an entry in the json dictionary

        user_watchlist = watchlist[str_user_id]         # Save the users watchlist 

    else: user_watchlist = []           # Returns an empty watchlist

    return user_watchlist
