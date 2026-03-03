from steam_web_api import Steam
import time
import json

game_dict = {}
steam = Steam("511BA295CDA8349CA246EDD6AD5ACA27")

username = input("Whats your username: ")

user_details = steam.users.search_user(username)


if isinstance(user_details, str):
    user_details = json.loads(user_details)


if "player" not in user_details:
    raise ValueError(f"User '{username}' not found or API error!")

user_id = user_details["player"]["steamid"]

owned_games = steam.users.get_owned_games(user_id, include_appinfo=True)

games = owned_games.get("games", [])

current_time = int(time.time())  # Unix timestamp siden det ble sånn 20k dager siden siden rtime_last_played er unix funksjon -Ludvig

for game in games:
    name = game.get("name")
    playtime_minutes = game.get("playtime_forever", 0)
    hours = playtime_minutes / 60

    last_played_timestamp = game.get("rtime_last_played", 0)

    if last_played_timestamp:
        seconds_since_played = current_time - last_played_timestamp
        days_since_played = seconds_since_played // 86400
    else:
        days_since_played = None  

    game_dict[name] = {
        "hours": hours,
        "days_since_played": days_since_played
    }

sorted_games = sorted(
    game_dict.items(),
    key=lambda x: x[1]["hours"],
    reverse=True
)

for name, info in sorted_games:
    if info["days_since_played"] is not None:
        print(f"{name} - {info['hours']:.1f} hours - {info['days_since_played']} days ago")
    else:
        print(f"{name} - {info['hours']:.1f} hours - Never played")
