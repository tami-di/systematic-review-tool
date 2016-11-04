from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)


@app.route('/categorias')
def categorias():
    cats = [{'name': 'categorias 1', 'id':1},{'name': 'categoria 2', 'id':2},{'name': 'categoria 3', 'id':3}]
    return render_template('categories.html',
                           categorias=cats)

@app.route('/data')
def data():
    cats = [{'name': 'categoria 1', 'id':1},{'name': 'categoria 2', 'id':2},{'name': 'categoria 3', 'id':3}]
    return render_template('data.html', categorias=cats)

