import os
from openai import OpenAI
from steam_web_api import Steam

def ask_chat(games):
    client = OpenAI(
        api_key="sk-CoEjC-ypfCaSob7S8dmSHA",
        base_url="https://hackathonlite-production.up.railway.app"
    )

    query = "Use this list of games to give 10 games that are similar. This list is a list of dictionaries, where the key is the name of the game, the first value is playtime forever and the second is rtime last played. Think about playtime and rtime last played when giving recommendations about other games. Here is the list: {games}"

    response = client.chat.completions.create(
        model="gemini-3-flash-preview",
        messages=[
            {"role": "assistant", "content": "Only list the names of the top 10 recommended games, prices and a link to the game in steam shop based on the data provided, also consider the games public rating on steam",
            "role": "assistant", "content": "The format should be [[game1_name, game1_price, game1_link], [game2_name, game2_price, game2_link]...[game10_name, game10_price, game10_link]]",
            "role": "user", "content": query}
        ]
    )

    return response.choices[0].message.content

def get_games(username):
    steam = Steam(os.environ.get("511BA295CDA8349CA246EDD6AD5ACA27"))

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
