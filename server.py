from flask import Flask, render_template, redirect, request
import html

app = Flask(__name__)
global recommendations 
recommendations = ""
recommendations_specific =""

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

@app.route("/Description")
def Description():
    return render_template("Description.html")

@app.route("/Recommended-Games")
def recommend_games():
    from get_recommendations import get_games, ask_chat
    global recommendations
    username = request.cookies.get("steamUsername")
    games = get_games(username)
    if games == False:
       return render_template("Recommended games.html", recommendations="It seems you don't own any games. Please try some games to see what you like before we can give any recommendations")    
    else:
        if recommendations == "":
            recommendations = ask_chat(games)
            recommendations = html.unescape(recommendations)
        else:
            print("waster")

    print(recommendations)
    return render_template("Recommended games.html", recommendations=recommendations)
     
@app.route("/Specific-Game-Recommendations", methods=['POST'])
def recommend_specific_games():
    from get_recommendations_specific import get_games, specific_ask_chat
    global recommendations_specific

    username = request.cookies.get("steamUsername")
    games = get_games(username)
    if games == False:
       return render_template("Specific Game Recommendation.html", recommendations="It seems you don't own any games. Please try some games to see what you like before we can give any recommendations")    
    else:
        if recommendations_specific == "":
            specific_query = request.form.get('query')
            recommendations_specific = specific_ask_chat(games, specific_query)
            recommendations_specific = html.unescape(recommendations_specific)
        else:
            print("waster")     

    print(recommendations_specific)  
    return render_template("Specific Game Recommendation.html", recommendations_specific=recommendations_specific)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

""""temporrary solution to avoid using up all the api calls, will be replaced with a database in the future, also makes it so the user can refresh the page without getting a new recommendation every time"""
@app.route('/about')
def about():
    return render_template("About.html")

@app.route('/specific')
def gotospecific():
    return render_template("Specific Game Recommendation.html")

@app.route('/general')
def gotogeneral():
    return render_template("Recommended games.html")

