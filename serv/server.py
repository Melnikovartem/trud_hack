from flask import Flask, render_template, request, redirect, url_for
from random import randint
import sys
sys.path.append('../vk_alg/')
from script import get_profession

app = Flask(__name__)


@app.route('/')
def main():
    return render_template("index.html")

@app.route('/search')
def search_get():
    id = request.args.get('id')
    if not id:
        return render_template("error.html")
    return render_template("search.html", id = id, proffession = get_profession(id))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
