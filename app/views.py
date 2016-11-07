from app import app
from flask import render_template
from flask import request

@app.route('/')
@app.route('/index')
def index():
    set_hidden = False
    search_input = request.args.get("searchinput")
    if search_input is not None:
        set_hidden = True
    if search_input == "":
        paper_id = ""
    else:
        paper_id = 1

    return render_template('index.html',
                           paper=paper_id,
                           set_form=set_hidden)


@app.route('/categorias')
def categorias():
    cats = [{'name': 'categorias 1', 'id':1},{'name': 'categoria 2', 'id':2},{'name': 'categoria 3', 'id':3}]
    return render_template('categories.html',
                           categorias=cats)

@app.route('/data')
def data():
    cats = [{'name': 'categoria 1', 'id':1},{'name': 'categoria 2', 'id':2},{'name': 'categoria 3', 'id':3}]
    return render_template('data.html', categorias=cats)

