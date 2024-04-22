import json


def get_json_data(path: str) -> None:
    with open(path, "r") as file:
        json_data = json.load(file)
    return json_data


def save_data(movies: object, watchlist: object) -> None:
    with open("data_json/movies.json", 'w') as file:
        movies_data = {title: movie.__dict__ for title, movie in movies.movies.items()}
        json.dump(movies_data, file, indent=4)

    with open("data_json/watchlist.json", 'w') as file:
        wl_data = {user: wl.watchlist for user, wl in watchlist.watchlists.items()}
        json.dump(wl_data, file, indent=4)