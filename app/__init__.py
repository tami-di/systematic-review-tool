from flask import Flask

app = Flask(__name__)
from api.db_api import connect_db
# initialize db
db = connect_db()
import views
import api