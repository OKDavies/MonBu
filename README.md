# MonBu

This Python script implements a movie bot for Discord, allowing users to interact with various movie-related commands. Users can rate movies, retrieve top-rated movies, manage watchlists, and more, all within Discord.


Installation

   1. Clone the repository:
   
      git clone https://github.com/yourusername/moviedb.git

   2. Install the required dependencies:
   
      pip install -r requirements.txt

   3. Ensure you have a .env file in the project directory containing your Discord bot token:
   
      DISCORD_TOKEN=your_discord_bot_token

      To get your own token follow the steps in this guide:
         https://discordpy.readthedocs.io/en/stable/discord.html



Usage

   To use the movie bot, run the MonBu.py script. Once the bot is running and connected to Discord, users can interact with it using commands prefixed with !.

Commands

   !help: Get a list of available commands and their usage.

   !ping: Check if the bot is active.

   !echo {content}: Repeat the provided message.

   !rate [movie title] *[x]: Rate a movie out of 10.

   !top [x]: Get a list of the top x rated movies.

   !mymovies: Get a list of all the movies you have rated.

   !usermovies @[user]: Get a list of all the movies a user has rated.

   !add [movie title]: Add a movie to your watchlist.

   !remove [movie title]: Remove a movie from your watchlist.

   !watchlist or !wl: View your watchlist, or tag a user to view theirs.

   !random: Get a random movie from your watchlist.



Example Usage

   To rate a movie:

      !rate The Matrix *9

   To view your watchlist:

      !watchlist


Integration with Discord

   The bot integrates with Discord using the discord.py library. It listens for messages in Discord channels and responds to messages that start with the command prefix !. The commands.py script contains the logic for handling commands.


Additional Context

   MonBu includes additional functionality through the following classes:

      InvalidMovie Exception:

         Raised when the movie cannot be found on IMDB.


      Scorecard Class:

         Manages movie ratings and averages.
         
         Adds movies and their ratings.
         
         Sorts movies by average rating.


      Movie Class:

         Represents individual movies with their ratings and averages.
         
         Calculates the average rating of a movie.


      Watchlists Class:

         Manages all user watchlists.
         
         Adds and retrieves watchlists for users.


      Watchlist Class:

         Represents a user's watchlist.
         
         Adds movies to the watchlist.
