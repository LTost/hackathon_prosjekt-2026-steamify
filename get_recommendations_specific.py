from openai import OpenAI
from steam_web_api import Steam

def specific_ask_chat(games, specific_query):
    client = OpenAI(
        api_key="sk-CoEjC-ypfCaSob7S8dmSHA",
        base_url="https://hackathonlite-production.up.railway.app"
    )

    query = f"""
You are a game recommendation assistant. Use the input list of games to recommend other games that are similar. 
Consider total playtime (playtime_forever), the tags of the games the user likes, and the game's public Steam rating and
most importantly the user's query if the query includes a specific genre only recommend games from that genre.

Here is the user's query: {specific_query} 
Here is the user's games (list of dictionaries, where each key is the game name, and the value is [playtime_forever_in_minutes, rtime_last_played_in_minutes]):

{games}

Return the **top 10 recommended games**. For each game, include:

1. Game name
2. Price in USD
3. Steam store link

Format the output clearly as numbered text, like this:

1. Game Name - $Price - year of release   <a href ="steam_link" target="_blank">Link</a>   thumbnail <br>
2. Game Name - $Price - year of release   <a href ="steam_link" target="_blank">Link</a>   thumbnail <br>
...
10. Game Name - $Price - year of release   <a href ="steam_link" target="_blank">Link</a>   thumbnail <br>


Do **not** include any extra explanation or text outside this format. 
Do **not** include any games that the user already owns.
Do **not** include any games that are not available on the Steam store.
Do **not** use one compact list format. Use the numbered format as shown above for clarity. '
Do  **not** include any games that do not fit the user's query if the query includes a specific genre.  
Do **not** include any games that arent on the steam store.
Make sure to double check the prices and thr link to the steam store
Make sure to cross check the users games and their tags to find what they liked about the game and use this to recommend new games, so its not just alot of the same games again and again


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
            game_info.append({game["name"]: [game["playtime_forever"]]})

    except KeyError:
        return False
    
    return game_info


### vi bør ha med pris og kanskje sorterings algoritme basert på rating og pris.
#### steam Key: 511BA295CDA8349CA246EDD6AD5ACA27
### openai key: sk-CoEjC-ypfCaSob7S8dmSHA
### all pip insalls required: pip install python-steam-api, pip install openai
