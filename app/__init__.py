from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/clinicdata?charset=utf8mb4" % quote('01312101220LtfA')
# 01312101220LtfA
# ducprotc123
app.secret_key = '(@*$&!(*@&$(*!&@()%&*(!@*%&(*!@&##)(!@$&(!@$&*^!@*(&$^@!&*^#!&*@#^*'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)
login = LoginManager(app=app)