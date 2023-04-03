from app import app
from flask import request, render_template


@app.route("/")
def index():
    return render_template("index.html")

@app.errorhandler(404)
def invalid_route(e):
    return render_template("page_not_found.html"), 404


@app.route("/callback", methods=["GET"])
def parse_code():
    try:
        code = request.args["code"]
    except:
        code = ""
        
    return render_template("index.html", code=code)
