import flask
from flask import Flask, render_template

import manager

app = Flask(__name__)


@app.route("/query/<kw>")
def get_price(kw):
    items = manager.get_item_list(kw)
    res = {"items": [a.to_dict() for a in items]}
    return flask.jsonify(res)


@app.route("/")
def home():
    return app.send_static_file("home.html")


if __name__ == '__main__':
    from waitress import serve

    serve(app, host="0.0.0.0", port=6768)
