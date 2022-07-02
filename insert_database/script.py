from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#conecatando ao banco de dados 
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = '[String de conexao do postgresql]'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#declarando a variavel db e a variavel de migração para o banco de dados
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#models
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

#abrindo o arqui ncms txt e criando os arrays de apoio
f = open("ncms.txt", "r")
array = []
array_temp = []
c = 0

#lendo o arquivo ncms.txt e separando em arrays com 1 antigo e seus respectivos novos
for l in f.readlines():
	c += 1
	linha = l.split(" ")
	temp1 = linha[0]
	temp2 = linha[len(linha)-1]
	linha = []
	linha.append(temp1)
	linha.append(temp2)
	if(c == 1):
		array_temp = linha
		array.append(array_temp)
	else:
	   if(linha[0] != ''):
	   	 	array.append(array_temp)
	   	 	array_temp = linha 
	   else:
	     array_temp.append(linha[1])


#criando dicionario para agrupar todos os subgrupos de ncms
dic = dict()
count = 1
c2 = 1


#dicionario de novos e antigos ncms
table_old = dict()
table_new = dict()



'''

O que o código a seguir faz? 

Pega cada lista de array da tabela array e cria um dicionario para cada item da subtabela.
Para facilitar a inserção no banco de dados os ncms antigos e novos, os dados são inseridos quase simultaneamente.

O for mais externo lê os ncms antigos e coloca no dicionario "table_old"

O for mais interno lê os ncms novos e coloca no dicionario "table_new", com a diferença que no campo
"id_antigo" é colocado o valor da variavel "count"

O valor da variavel count é o mesmo valor do ncm do for mais externo, por isso a relação bate. 
A "count" está sendo incrementada com base nos ncms antigos

'''

#acessando o array com todos os grupos de ncms e fazendo o apontamento entre os ncms
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


#test
s = input("Digite o codigo antigo que vc quer pesquisar")

data_ncm = NcmNewModel.query.join(NcmOldModel, NcmOldModel.id==NcmNewModel.old_id) \
                                 .where(NcmOldModel.code == s) \
                                 .order_by(NcmOldModel.id).all()

for data in data_ncm:
	print(f"{data.code} ")

