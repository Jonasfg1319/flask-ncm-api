from flask import jsonify
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin


app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")