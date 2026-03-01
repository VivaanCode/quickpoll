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
        return render_template("404.html"), 404

@app.route("/create")
def create():
    question = request.args.get("question")
    options = request.args.getlist("options") # getlist is a very handy tool
    if question and options:
        id = api.createPoll(question, *options)
        return render_template("poll.html", poll=api.getPoll(id), id=id)
    return render_template("400.html"), 400

@app.route("/poll/<id>/vote")
def vote(id):
    option = request.args.get("option")
    try:
        newOption = int(option)
    except ValueError:
        return render_template("400.html"), 400
    if option:
        api.vote(id, newOption)
        return render_template("poll.html", poll=api.getPoll(id), id=id)
    return render_template("400.html"), 400

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(400)
def bad_request(e):
    return render_template("400.html"), 400

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500

# @app.errorhandler(Exception)
# def test(e):
#     return render_template("generic_error.html", e), 520 # i just searched up "generic error http code"

if __name__ == "__main__":
    app.run()