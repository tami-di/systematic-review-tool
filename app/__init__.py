from flask import Flask
app = Flask(__name__)
import MySQLdb
from app.db_config import db_config


def connect_db():
    db = MySQLdb.connect(host=db_config['host'], user=db_config['user'],
                         passwd=db_config['passwd'], db=db_config['db'])
    return db
db = connect_db()
import views
import api





