from flask import Flask, send_file

app = Flask(__name__)

@app.route("/Main")
def home():
    return send_file("Main.html")

@app.route("/Username input")
def login():
    return send_file("Username input.html")

@app.route("/General")
def general():
    return send_file("General.html")

@app.route("/Specific")
def specific():
    return send_file("Specific.html")

@app.route("/How to")
def howto():
    return send_file("Howto.html")

@app.errorhandler(404)
def page_not_found(e):
    return send_file("404.html"), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)