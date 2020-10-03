from flask import request

from webhooks import app


@app.route("/", methods=["GET", "POST"])
def landing():
    if request.method == "POST":
        app.logger.info("I received some JSON data")
    return "Nothing here..."
