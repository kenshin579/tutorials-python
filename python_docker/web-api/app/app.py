#!/usr/bin/env python3

from flask import Flask
import os

app = Flask(__name__)


@app.route("/")
def hello():
    return "Flask inside Docker!!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10500))
    app.run(debug=True, host='0.0.0.0', port=port)
