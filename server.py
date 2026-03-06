from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route("/Main")
def home():
    return render_template("Main.html")

@app.route("/Username-input")
def login():
    return render_template("Username input.html")

@app.route("/General-Recommendations")
def general():
    from get_recommendations import get_games, ask_chat
    username = request.cookies.get("steamUsername")

    games = get_games(username)
    recommendations = ask_chat(games)

    return render_template("General.html", recommendations)

@app.route("/Specific-Recommendations")
def specific():
    return render_template("Specific.html")

@app.route("/How-to")
def howto():
    return render_template("Howto.html")

@app.route("/")
def root():
    return redirect("/Main")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)