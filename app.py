import flask
from flask import Flask, render_template

import manager

app = Flask(__name__)


@app.route("/query/<kw>")
def get_price(kw):
    items = []
    args = kw.split("@")

    en_tesco = True
    en_sains = True
    en_poundland = True
    limit = 30
    if len(args) > 1:
        for arg in args:
            arg: str
            if arg:
                if arg.startswith("l"):
                    limit = int(arg[1:])
                elif arg.startswith("o"):
                    enable_list = arg.split(" ")
                    en_tesco = False
                    en_sains = False
                    en_poundland = False
                    for en_str in enable_list[1:]:
                        if en_str == "t":
                            en_tesco = True
                        elif en_str == "s":
                            en_sains = True
                        elif en_str == "p":
                            en_poundland = True
                elif arg.startswith("d"):
                    dis_list = arg.split(" ")
                    for en_str in dis_list[1:]:
                        if en_str == "t":
                            en_tesco = False
                        elif en_str == "s":
                            en_sains = False
                        elif en_str == "p":
                            en_poundland = False

    kw = args[-1]
    items = manager.get_item_list(kw, limit, en_tesco, en_sains, en_poundland)
    res = {"items": [a.to_dict() for a in items]}
    return flask.jsonify(res)


@app.route("/")
def home():
    return app.send_static_file("home.html")


if __name__ == '__main__':
    from waitress import serve

    serve(app, host="0.0.0.0", port=6768)
