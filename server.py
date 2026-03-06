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
    recommendations = ask_chat(games)
    #recommendations = html.unescape(recommendations)

    return render_template("Recommended games.html", games=recommendations)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404