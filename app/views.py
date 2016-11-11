from app import app, db
from flask import render_template
from flask import request
from api.views import request_headers_from_cat_aux
import api.db_api as db_api



@app.route('/')
@app.route('/index')
def index():
    set_hidden = False
    search_input = request.args.get("searchinput")
    if search_input is not None:
        paper_id = db_api.get_paper_id_where_title_exactly(db, search_input)
        set_hidden = True
    else:
        paper_id = ""
    return render_template('index.html',
                           paper=paper_id,
                           set_form=set_hidden)


@app.route('/categorias')
def categorias():
    cats = db_api.get_all_categories_as_dict_array(db)
    data_types = db_api.get_columns_data_types()
    return render_template('categories.html',
                           categorias=cats,
                           data_types=data_types)

@app.route('/data')
def data():
    cats = db_api.get_all_categories_as_dict_array(db)
    return render_template('data.html', categorias=cats)

@app.route('/search',  methods=['POST','GET'])
def search():
    if request.method == 'POST':
        checkbox_values = request.form.getlist('checkboxes')
        paper_properties = [{'name':'title','type':'varchar'},
                            {'name':'authors','type':'varchar'},
                            {'name':'abstract','type':'text'},
                            {'name':'summary','type':'text'},
                            {'name':'categoria 1','type':'category',"id":1}]
        values = {}
        categories_properties = {}
        for prop in paper_properties:
            if not prop['type'] == 'category':
                values[prop['name']] = request.form.get("search-"+(prop['name']).replace(" ","-"))
                print prop['name'],":",values[prop['name']]
            else:
                cat_prop = request_headers_from_cat_aux(prop['id'])
                categories_properties[prop['id']] = cat_prop
                for c_prop in cat_prop:
                    values[prop['name']+c_prop['name']] = request.form.get("search-"+(prop['name']).replace(" ","-")
                                                                           +"-"+ (c_prop['name']).replace(" ","-"))
                    print prop['name'],c_prop['name'],":",values[prop['name']+c_prop['name']]
        print "Checkbox values:",checkbox_values
        # here the search is made and then we render the template again
        headers = ['title','abstract','summary','categoria 1']
        data = [{'title':'El paper 1',
                    'authors':'autor 1; autor 2; autor 3',
                    'abstract':'El paper dice cositas muy choris.',
                    'summary':'El paper dice cositas como cuackers y miau.',
                    'categoria 1':'cucurilo'},
                   {'title':'El paper 2',
                    'authors':'autor 5',
                    'abstract':'El paper dice cositas. Hace cuack.',
                    'summary':'Cuack cuack cuack',
                    'categoria 1':'cucurilo'}]
        results = {'headers':headers,'data':data}
        print values
    else:
        values = {}
        results = {}
    return render_template('search.html', dict=values, results=results)

@app.route('/api/add_data/search/paper/', methods=['POST'])
def search_paper():
    checkbox_values = request.form.getlist('checkboxes')
    paper_properties = [{'name':'title','type':'varchar'},
                        {'name':'authors','type':'varchar'},
                        {'name':'abstract','type':'text'},
                        {'name':'summary','type':'text'},
                        {'name':'categoria 1','type':'category',"id":1}]
    values = {}
    categories_properties = {}
    for prop in paper_properties:
        if not prop['type'] == 'category':
            values[prop['name']] = request.form.get("search-"+(prop['name']).replace(" ","-"))
            print prop['name'],":",values[prop['name']]
        else:
            cat_prop = request_headers_from_cat_aux(prop['id'])
            categories_properties[prop['id']] = cat_prop
            for c_prop in cat_prop:
                values[prop['name']+c_prop['name']] = request.form.get("search-"+(prop['name']).replace(" ","-")
                                                                       +"-"+ (c_prop['name']).replace(" ","-"))
                print prop['name'],c_prop['name'],":",values[prop['name']+c_prop['name']]
    print "Checkbox values:",checkbox_values
    #here the search is made and then we render the template again
    results = []
    return render_template('search.html', dict=values, results=results)


