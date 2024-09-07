#imports
from flask import Flask
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy

#my app
app = Flask(__name__)


@app.route("/")
def index():
    return "testing 123"


if __name__ in "__main__":
    app.run(debug=True)

