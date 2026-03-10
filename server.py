from flask import Flask, render_template, redirect, request
import html

app = Flask(__name__)

@app.route("/Main")
def home():
    return render_template("Main.html")

@app.route("/Username-input")
def login():
    return render_template("Username input.html")

@app.route("/General-Recommendations")
def general():
    return render_template("General.html")

@app.route("/Specific-Recommendations")
def specific():
    return render_template("Specific.html")

@app.route("/How-to")
def howto():
    return render_template("Howto.html")

@app.route("/")
def root():
    return redirect("/Main")

@app.route("/Recommended-Games")
def recommend_games():
    from get_recommendations import get_games, ask_chat

    username = request.cookies.get("steamUsername")
    games = get_games(username)
    if games == False:
       return render_template("Recommended games.html", recommendations="It seems you don't own any games. Please try some games to see what you like before we can give any recommendations")    
    else:
        recommendations = ask_chat(games)
        recommendations = html.unescape(recommendations)

    return render_template("Recommended games.html", recommendations=recommendations)
     
@app.route("/Specific-Game-Recommendations")
def recommend_specific_games():
    from get_recommendations_specific import get_games, specific_ask_chat

    username = request.cookies.get("steamUsername")
    games = get_games(username)
    if games == False:
       return render_template("Specific Game Recommendation.html", games="It seems you don't own any games. Please try some games to see what you like before we can give any recommendations")    
    else:
        specific_query = request.cookies.get("specific_query")
        recommendations = specific_ask_chat(games, specific_query)
        recommendations = html.unescape(recommendations)

    return render_template("Specific Game Recommendation.html", recommendations=recommendations)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404