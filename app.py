import flask
from flask import Flask

import manager

app = Flask(__name__)


@app.route("/query/<kw>")
def get_price(kw):
    args = kw.split("@")

    en_tesco = True
    en_sains = True
    en_poundland = True
    en_waitrose = True
    limit = 30
    expect = -1.0
    if len(args) > 1:
        for arg in args[:-1]:
            arg: str
            if arg:
                if arg.startswith("l"):
                    limit = int(arg[1:])
                elif arg.startswith("o"):
                    enable_list = arg.split(" ")
                    en_tesco = False
                    en_sains = False
                    en_poundland = False
                    en_waitrose = False
                    for en_str in enable_list[1:]:
                        if en_str == "t":
                            en_tesco = True
                        elif en_str == "s":
                            en_sains = True
                        elif en_str == "p":
                            en_poundland = True
                        elif en_str == "w":
                            en_waitrose = True
                elif arg.startswith("d"):
                    dis_list = arg.split(" ")
                    for en_str in dis_list[1:]:
                        if en_str == "t":
                            en_tesco = False
                        elif en_str == "s":
                            en_sains = False
                        elif en_str == "p":
                            en_poundland = False
                        elif en_str == "w":
                            en_waitrose = False
                elif arg.startswith("p"):
                    expect = float(arg[1:])

    kw = args[-1]
    res = {}
    if kw:
        items = manager.get_item_list(kw, limit, expect, en_tesco, en_sains, en_poundland, en_waitrose)
        res = {"items": [a.to_dict() for a in items]}
    return flask.jsonify(res)


@app.route("/")
def home():
    return app.send_static_file("home.html")


if __name__ == '__main__':
    from waitress import serve

    serve(app, host="0.0.0.0", port=6768)
