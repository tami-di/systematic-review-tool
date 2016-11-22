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
        # obtain data
        checkbox_values = request.form.getlist('checkboxes')
        paper_properties = db_api.get_paper_properties(db)

        # values maintains the previous field values on the search form
        values = {}
        paper_values = []
        authors_value = ""
        categories_values = []
        for prop in paper_properties:
            if not prop['type'] == 'category':
                if prop['name'] == 'authors':
                    field_name = "search-"+(prop['name']).replace(" ","-")
                    authors_value = request.form.get(field_name)
                    values[prop['name']] = request.form.get(field_name)
                else:
                    field_name = "search-"+(prop['name']).replace(" ","-")
                    paper_values.append({'id_name':(prop['name']).replace(" ","_"),
                                         'value':request.form.get(field_name)})
                    values[prop['name']] = request.form.get(field_name)
            else:
                category_values = []
                full_data = db_api.get_data_from_category_as_headers_and_column_data(db, prop['id'])
                cat_prop = full_data['headers']
                for c_prop in cat_prop:
                    if c_prop['name'] == 'id':
                        continue
                    if c_prop['type'] == 'subcat':
                        field_name = "search-"+(prop['name']).replace(" ","-")+"-"+ (c_prop['name']).replace(" ","-")
                        value = request.form.get(field_name)
                        category_values.append({'subcat_id':c_prop['id'],
                                                'rel_with_cat':c_prop['rel_with_cat'],
                                                'name_value':value,
                                                'is_subcat':True})

                        values[prop['name']+c_prop['name']] = value
                    else:
                        field_name = "search-"+(prop['name']).replace(" ","-")+"-"+ (c_prop['name']).replace(" ","-")
                        value = request.form.get(field_name)
                        category_values.append({'id_name':(c_prop['name']).replace(" ","_"),
                                                'value':value,
                                                'is_subcat':False})
                        values[prop['name']+c_prop['name']] = value
                categories_values.append({'cat_id':prop['id'],'values':category_values})
        # here the search is made and then we render the template again
        paper_ids = db_api.search_papers_id(db, paper_values, authors_value, categories_values)

        headers = ['title']+[str(a) for a in checkbox_values]
        data = []
        for paper_id in paper_ids:
            paper_properties = db_api.get_paper_properties_and_values_on_table_format(db, paper_id)
            data.append(paper_properties)

        results = {'headers':headers,'data':data}
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
        else:
            cat_prop = request_headers_from_cat_aux(prop['id'])
            categories_properties[prop['id']] = cat_prop
            for c_prop in cat_prop:
                values[prop['name']+c_prop['name']] = request.form.get("search-"+(prop['name']).replace(" ","-")
                                                                       +"-"+ (c_prop['name']).replace(" ","-"))
    #here the search is made and then we render the template again
    results = []
    return render_template('search.html', dict=values, results=results)


