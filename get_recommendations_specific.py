from openai import OpenAI
from steam_web_api import Steam

def specific_ask_chat(games, specific_query):
    client = OpenAI(
        api_key="sk-CoEjC-ypfCaSob7S8dmSHA",
        base_url="https://hackathonlite-production.up.railway.app"
    )

    query = fquery = f"""
You are a Steam game recommendation assistant.

Your task is to recommend games similar to the user's existing games and their search query.

INPUTS
------
User query:
{specific_query}

User's owned games:
Each item is a dictionary where:
key = game name
value = [playtime_forever_in_minutes, rtime_last_played_in_minutes]

{games}


RECOMMENDATION RULES
--------------------
Use the following signals to determine similarity:

1. The user's query (MOST IMPORTANT)
   - If the query specifies a genre (e.g., roguelike, FPS, RPG, strategy), ONLY recommend games from that genre.

2. Playtime
   - Games with higher playtime indicate stronger preference.

3. Game tags / genres
   - Recommend games with similar tags to the user's most played games.

4. Steam ratings
   - Prefer games with strong public Steam ratings.

RESTRICTIONS
------------
- Recommend EXACTLY 10 games.
- Do NOT recommend games the user already owns.
- Only recommend games available on the Steam store.
- Do NOT recommend games outside the requested genre if a genre is specified.
- Do NOT include explanations, commentary, or markdown.
- Do NOT output anything except the list.


OUTPUT FORMAT
-------------
Return the recommendations EXACTLY in the following numbered format:

1. Game Name - $Price - Year of release - <a href="steam_link" target="_blank">Link</a> <br>
2. Game Name - $Price - Year of release - <a href="steam_link" target="_blank">Link</a> <br>
3. Game Name - $Price - Year of release - <a href="steam_link" target="_blank">Link</a> <br>
4. Game Name - $Price - Year of release - <a href="steam_link" target="_blank">Link</a> <br>
5. Game Name - $Price - Year of release - <a href="steam_link" target="_blank">Link</a> <br>
6. Game Name - $Price - Year of release - <a href="steam_link" target="_blank">Link</a> <br>
7. Game Name - $Price - Year of release - <a href="steam_link" target="_blank">Link</a> <br>
8. Game Name - $Price - Year of release - <a href="steam_link" target="_blank">Link</a> <br>
9. Game Name - $Price - Year of release - <a href="steam_link" target="_blank">Link</a> <br>
10. Game Name - $Price - Year of release - <a href="steam_link" target="_blank">Link</a> <br>
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
