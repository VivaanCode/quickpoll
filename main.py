from flask import Flask, render_template, request
import api

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/poll/<id>")
def poll(id):
    poll = api.getPoll(id)
    if poll:
        return render_template("poll.html", poll=poll, id=id)
    else:
        return "page not found", 404 # update to custom 404 page

@app.route("/create")
def create():
    question = request.args.get("question")
    options = request.args.getlist("options") # getlist is a very handy tool
    if question and options:
        id = api.createPoll(question, *options)
        return f"<a href='/poll/{id}'>Poll created!</a>"
    return "Bad request", 400

if __name__ == "__main__":
    app.run()