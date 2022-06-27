from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


def __init__():
	pass

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://mqikusitjpynqg:e42dea1a5eb3e68cc4e54ee5bf0341be5a5ee73e2ce90182cb965a11a518210a@ec2-44-197-128-108.compute-1.amazonaws.com:5432/daq2vrbklcvea0'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

