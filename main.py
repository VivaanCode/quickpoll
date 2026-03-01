from flask import Flask, render_template, request, redirect
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

    if len(options) < 2 or len(options) > 10:
        return render_template("length.html"), 400
    if len(question) < 1 or len(question) > 200:
        return render_template("length.html"), 400

    if question and options:
        id = api.createPoll(question, *options)
        return redirect(f"/poll/{id}")
    return render_template("400.html"), 400

@app.route("/poll/<id>/vote")
def vote(id):
    option = request.args.get("option")
    try:
        newOption = int(option)
    except (TypeError, ValueError):
        return render_template("400.html"), 400
    if option:
        if api.vote(id, newOption):
            return redirect(f"/poll/{id}/view")
        return render_template("400.html"), 400
    return render_template("400.html"), 400

@app.route("/poll/<id>/view")
def view(id):
    poll = api.getPoll(id)
    if poll:
        return render_template("view.html", poll=poll, id=id)
    else:
        return render_template("404.html"), 404

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