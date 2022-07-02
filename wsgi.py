from flask import Flask
from flask import jsonify
from flask import Flask, render_template
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


#CONFIG
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = '[String de conexao do postgresql]'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#MODELS
class NcmOldModel(db.Model):
  __tablename__ = 'old_ncm'
  id = db.Column(db.Integer, primary_key=True)
  code = db.Column(db.String())
  

  def __init__(self, code):
   self.code = code


class NcmNewModel(db.Model):
  __tablename__ = 'new_ncm'
  id = db.Column(db.Integer, primary_key=True)
  code = db.Column(db.String())
  old_id = db.Column(db.Integer)
  

  def __init__(self, code, old_id):
   self.code = code
   self.old_id = old_id



#ROUTES
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/ncms_antigos")
@cross_origin()
def old_All():
	all = NcmOldModel.query.all()
	results = [{ "id" : ncm.id,"code" : ncm.code } for ncm in all]
	return jsonify(results)



@app.route("/ncms_novos")
@cross_origin()
def new_all():
	all = NcmNewModel.query.all()
	results = [{ "id" : ncm.id,"code" : ncm.code,"old_id": ncm.old_id} for ncm in all]
	return jsonify(results)


@app.route("/<string:code>")
@cross_origin()
def search_relathionship(code):
	data_ncm = NcmNewModel.query.join(NcmOldModel, NcmOldModel.id==NcmNewModel.old_id).where(NcmOldModel.code == code).order_by(NcmOldModel.id).all()
	results = [{ "id" : ncm.id,"code" : ncm.code } for ncm in data_ncm]
	return jsonify(results)

@app.route("/docs")
def docs():
	return render_template("doc.html")


@app.route("/sobre")
def about():
	return render_template("sobre.html")