from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://mqikusitjpynqg:e42dea1a5eb3e68cc4e54ee5bf0341be5a5ee73e2ce90182cb965a11a518210a@ec2-44-197-128-108.compute-1.amazonaws.com:5432/daq2vrbklcvea0'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


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


f = open("ncms.txt", "r")
array = []
array_temp = []
c = 0

for l in f.readlines():
	c += 1
	linha = l.split(" ")
	temp1 = linha[0]
	temp2 = linha[len(linha)-1]
	linha = []
	linha.append(temp1)
	linha.append(temp2)
	#print(f"Minha linha é {linha}")
	if(c == 1):
		array_temp = linha
		array.append(array_temp)
	else:
	   if(linha[0] != ''):
	   	 	array.append(array_temp)
	   	 	array_temp = linha 
	   else:
	     array_temp.append(linha[1])

dic = dict()
count = 1
c2 = 1



table_old = dict()
table_new = dict()

for i in range(len(array)):
	ncms_old = dict()
	novos = []
	ncms_old["id"] = count
	ncm = array[i][0].replace(".","")
	ncms_old["codigo"] = ncm
	ncm_db = NcmOldModel(ncms_old["codigo"])
	db.session.add(ncm_db)
	db.session.commit()
	table_old[count] = ncms_old
	for k in range(len(array[i])):
		if(k != 0):
			ncms_new = dict()
			ncms_new["id"] = c2
			ncm2 = array[i][k].replace(".","")
			ncm2 = ncm2.replace("\n","")
			ncms_new["codigo"] = ncm2
			ncms_new["id_antigo"] = count
			ncm_db_update = NcmNewModel(ncms_new["codigo"], ncms_new["id_antigo"])
			db.session.add(ncm_db_update)
			db.session.commit()
			c2+= 1
			table_new[c2] = ncms_new
			novos.append(array[i][k])
	dic[array[i][0]] = novos
	count+=1



s = input("Digite o codigo antigo que vc quer pesquisar")

data_ncm = NcmNewModel.query.join(NcmOldModel, NcmOldModel.id==NcmNewModel.old_id) \
                                 .where(NcmOldModel.code == s) \
                                 .order_by(NcmOldModel.id).all()

for data in data_ncm:
	print(f"{data.code} ")

