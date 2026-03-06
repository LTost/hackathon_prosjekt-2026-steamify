from flask import Flask, render_template, redirect, request
app = Flask(__name__)

@app.route("/Main")

@@ -10,9 +9,16 @@ def home():
def login():
    return render_template("Username input.html")

@app.route("/General-Recommendations")
def general():
    return render_template("General.html")
@app.route("/Specific-Recommendations")
def specific():

@@ -26,16 +32,6 @@ def howto():
def root():
    return redirect("/Main")

@app.route("/Recommended-Games")
def recommend_games():
    from get_recommendations import get_games, ask_chat

    username = request.cookies.get("steamUsername")
    games = get_games(username)
    recommendations = ask_chat(games)

    return render_template("Recommended games.html", games=recommendations)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)