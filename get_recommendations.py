from openai import OpenAI
from steam_web_api import Steam

def ask_chat(games):
    client = OpenAI(
        api_key="sk-CoEjC-ypfCaSob7S8dmSHA",
        base_url="https://hackathonlite-production.up.railway.app"
    )

    query = f"""
You are a game recommendation assistant. Use the input list of games to recommend other games that are similar.
Consider the total playtime (playtime_forever), recent playtime (rtime last played), and the game's public rating on Steam.

Here is the list of games the user owns (format: a list of dictionaries, where each key is the game name,
and the value is a list: [playtime_forever_in_minutes, rtime_last_played_in_minutes]):

{games}

Using this data, return the top 10 recommended games. Include only the following for each game:
[game_name, price_in_USD, Steam_store_link].

Output format should be a list of 10 lists like this:
[[game1_name, game1_price, game1_link], [game2_name, game2_price, game2_link], ..., [game10_name, game10_price, game10_link]].
Do not include any text outside this list.
"""

    response = client.chat.completions.create(
        model="gemini-3-flash-preview",
        messages=[
            {"role": "assistant", "content": "Only list the names of the top 10 recommended games, prices and a link to the game in steam shop based on the data provided, also consider the games public rating on steam",
            "role": "assistant", "content": "The format should be [[game1_name, game1_price, game1_link], [game2_name, game2_price, game2_link]...[game10_name, game10_price, game10_link]] without any other text",
            "role": "user", "content": query}
        ]
    )

    return response.choices[0].message.content

def get_games(username):
    steam = Steam("511BA295CDA8349CA246EDD6AD5ACA27")

    user_details = steam.users.search_user(username)
    user_id = user_details["player"]["steamid"]

    owned_games = steam.users.get_owned_games(user_id)
    game_info = []
    
    try:
        for game in owned_games["games"]:
            game_info.append({game["name"]: [game["playtime_forever"], game["rtime_last_played"]]})

    except KeyError:
        return "It seems you don't have any games installed. Please try some games to see what you like before we can give any recommendations"
    
    return game_info

### vi bør ha med pris og kanskje sorterings algoritme basert på rating og pris.
#### steam Key: 511BA295CDA8349CA246EDD6AD5ACA27
### openai key: sk-CoEjC-ypfCaSob7S8dmSHA
### all pip insalls required: pip install python-steam-api, pip install openai
