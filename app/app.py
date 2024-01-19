__author__ = 'ivana'

#Import Flask librery
from flask import *
from flask_mysqldb import MySQL
#Import field
from db_config import db_config
import api

#--------------------------------------- server connection ----------------------------------------
app = Flask(__name__)
app.run(port=3000)

app.config['MYSQL_HOST'] = db_config['host']
app.config['MYSQL_USER'] = db_config['user']
app.config['MYSQL_PASSWORD'] = db_config['passwd']
app.config['MYSQL_DB'] = db_config['db']

db = MySQL(app)


#--------------------------------------------- routes ---------------------------------------------

@app.route("/")
@app.route('/index')
def index():
    set_hidden = False
    search_input = request.args.get("searchinput")
    if search_input is not None:
        paper_id = api.get_paper_id_by_value(db, search_input)
        set_hidden = True
    else:
        paper_id = ""
    return render_template('index.html',
                           paper=paper_id,
                           set_form=set_hidden)

   

@app.route('/getSuggestions', methods=['GET'])
def getSuggestions():
    s = api.get_suggestions(db)
    return s



@app.route('/categorias')
def categorias():
    cats = api.get_all_categories_as_dict_array(db)
    data_types = api.get_columns_data_types()
    return render_template('categories.html',
                           categorias=cats,
                           data_types=data_types)

@app.route('/data')
def data():
    cats = api.get_all_categories_as_dict_array(db)
    data_types = api.get_columns_data_types()
    return render_template('data.html', categorias=cats,
                           data_types=data_types)


@app. route('/autores')
def autores():
    return render_template('authors.html')


@app.route('/copy',  methods=['POST','GET'])
def copy():
    if request.method == 'POST':
        # obtain data
        checkbox_values = request.form.getlist('checkboxes')
        paper_properties = api.get_paper_properties(db)
        # values maintains the previous field values on the search form
        values = {}
        paper_values = []
        authors_value = ""
        categories_values = []
        for prop in paper_properties:
            if not prop['type'] == 'category':
                if prop['name'] == 'authors':
                    field_name = "search-"+(prop['name']).replace(" ","-")
                    authors_value = request.form.get('query')
                    values[prop['name']] = request.form.get('query')
                else:
                    field_name = "search-"+(prop['name']).replace(" ","-")
                    paper_values.append({'id_name':(prop['name']).replace(" ","_"),
                                         'value':request.form.get('query')})
                    values[prop['name']] = request.form.get(field_name)
            else:
                category_values = []
                full_data = api.get_data_from_category_as_headers_and_column_data(db, prop['id'])
                cat_prop = full_data['headers']
                for c_prop in cat_prop:
                    if c_prop['name'] == 'id':
                        continue
                    if c_prop['type'] == 'subcat':
                        field_name = "search-"+(prop['name']).replace(" ","-")+"-"+ (c_prop['name']).replace(" ","-")
                        value = request.form.get('query')
                        category_values.append({'subcat_id':c_prop['id'],
                                                'rel_with_cat':c_prop['rel_with_cat'],
                                                'name_value':value,
                                                'is_subcat':True})

                        values[prop['name']+c_prop['name']] = value
                    else:
                        field_name = "search-"+(prop['name']).replace(" ","-")+"-"+ (c_prop['name']).replace(" ","-")
                        value = request.form.get('query')
                        category_values.append({'id_name':(c_prop['name']).replace(" ","_"),
                                                'value':value,
                                                'is_subcat':False})
                        values[prop['name']+c_prop['name']] = value

                categories_values.append({'cat_id':prop['id'],'values':category_values})
        # here the search is made and then we render the template again
        # search_input = request.form.get("searchinput")
        paper_ids = api.search_papers_id2(db,paper_values, authors_value, categories_values)
        headers = ['title']+[str(a) for a in checkbox_values]
        data = []
        for paper_id in paper_ids:
            paper_properties = api.get_paper_properties_and_values_on_table_format(db, paper_id)
            data.append(paper_properties)

        results = {'headers':headers,'data':data}
    else:
        values = {}
        results = {}
    return render_template('copy.html', dict=values, results=results)


@app.route('/search',  methods=['POST','GET'])
def search():
    if request.method == 'POST':
        # obtain data
        checkbox_values = request.form.getlist('checkboxes')
        paper_properties = api.get_paper_properties(db)
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
                full_data = api.get_data_from_category_as_headers_and_column_data(db, prop['id'])
                cat_prop = full_data['headers']
                for c_prop in cat_prop:
                    if c_prop['name'] == 'id':
                        continue
                    if c_prop['type'] == 'subcat':
                        field_name = "search-"+(prop['name']).replace(" ","-")+"-"+ (c_prop['name']).replace(" ","-")
                        print(field_name)
                        value = request.form.get(field_name)
                        category_values.append({'subcat_id':c_prop['id'],
                                                'rel_with_cat':c_prop['rel_with_cat'],
                                                'name_value':value,
                                                'is_subcat':True})

                        values[prop['name']+c_prop['name']] = value
                    else:
                        field_name = "search-"+(prop['name']).replace(" ","-")+"-"+ (c_prop['name']).replace(" ","-")
                        print(field_name)
                        value = request.form.get(field_name)
                        category_values.append({'id_name':(c_prop['name']).replace(" ","_"),
                                                'value':value,
                                                'is_subcat':False})
                        values[prop['name']+c_prop['name']] = value

                categories_values.append({'cat_id':prop['id'],'values':category_values})
        # here the search is made and then we render the template again
        paper_ids = api.search_papers_id(db, paper_values, authors_value, categories_values)
        headers = ['title']+[str(a) for a in checkbox_values]
        data = []
        for paper_id in paper_ids:
            paper_properties = api.get_paper_properties_and_values_on_table_format(db, paper_id)
            data.append(paper_properties)

        results = {'headers':headers,'data':data}
    else:
        values = {}
        results = {}
    return render_template('search.html', dict=values, results=results)


#------------------------------------------- routes api -------------------------------------------

@app.route('/api/request/headers+subcategories/<cat_id>')
def subcategories(cat_id):
    subcats = api.get_all_properties_from_category_as_dict_array(db, cat_id)
    return jsonify(subcategories=subcats)

@app.route('/api/request/headers+subcategories/norep/<cat_id>')
def subcategories_without_interaction(cat_id):
    subcats = api.get_all_properties_from_category_as_dict_array(db, cat_id)
    dict_array = api.remove_subcategories_duplicated(subcats)
    return jsonify(subcategories=dict_array)

@app.route('/api/request/headers/subcategory/<subcat_id>')
def subcategory_data(subcat_id):
    subcats_data = api.get_subcategory_data(db, subcat_id)
    return jsonify(subcategory_data=subcats_data)


@app.route('/api/add/subcategory/', methods=['POST'])
def add_subcategory():
    # request.form is a dictionary with the form stuff
    select_existig_subcat_id = request.form.get('select-existig-subcat')
    subcat_name = request.form.get('subcat-name')
    category_of_subcategory_id = int(request.form.get('category-of-subcategory'))
    cat_interaction_with_subcat = (str(request.form.get('cat-interaction-with-subcat'))).replace(" ","_")
    # Here you do what you want with the info received
    if select_existig_subcat_id == str(0):
        api.create_subcategory(db,subcat_name,category_of_subcategory_id,cat_interaction_with_subcat)
    else:
        api.create_interaction_for_existing_subcategory(db,category_of_subcategory_id,cat_interaction_with_subcat,
                                                           select_existig_subcat_id)
    return redirect(request.referrer)


@app.route('/api/request/data/subcategories/category/<cat_id>')
def get_subcategories_name_and_if_from_category(cat_id):
    subcats_ids = api.get_all_subcategories_id_of_category_as_array(db, cat_id)
    dict_array = []
    for subcat_id in subcats_ids:
        subcat_name = api.get_content_name_from_id(db,subcat_id)
        dict_array.append({'subcat_id':subcat_id,'subcat_name':subcat_name})
    # request.form is a dictionary with the form stuff
    return jsonify(subcategories_info=dict_array )


@app.route('/api/add/category/', methods=['POST'])
def add_category():
    # request.form is a dictionary with the form stuff
    cat_name = request.form.get('cat-name')
    cat_description = request.form.get('cat-description')
    # Here you do what you want with the info received
    api.create_category(db, cat_name, cat_description)
    return redirect(request.referrer)

@app.route('/api/add/column/category/<cat_id>', methods=['POST'])
def add_column_to_category(cat_id):
    # request.form is a dictionary with the form stuff
    col_name = request.form.get('col-name')
    col_data = request.form.get('select-data-type')
    # Here you do what you want with the info received
    api.add_column_to_category(db, cat_id, col_name, col_data)
    return redirect(request.referrer)

@app.route('/api/add_column/<subcat_id>/subcategory', methods=['POST'])
def add_column_to_subcategory(subcat_id):
    # request.form is a dictionary with the form stuff
    col_name = request.form.get('col-name')
    col_data = request.form.get('select-data-type')
    # Here you do what you want with the info received
    api.add_column_to_subcategory(db, subcat_id, col_name, col_data)
    return redirect(request.referrer)


@app.route('/api/delete/category/<cat_id>', methods=['POST'])
def delete_category(cat_id):
    # Here you do what you want with the info received
    api.delete_category_by_id(db,cat_id)
    return redirect(request.referrer)


@app.route('/api/delete/subcategory/<subcat_id>/category/<cat_id>', methods=['POST'])
def delete_subcategory(subcat_id,cat_id):
    # Here you do what you want with the info received
    api.delete_subcategory_by_id(db, subcat_id,cat_id=cat_id)
    return redirect(request.referrer)


@app.route('/api/delete/column/<column_name>/category/<cat_id>', methods=['POST'])
def delete_category_column(cat_id,column_name):
    # Here you do what you want with the info received
    api.delete_category_column(db, cat_id,column_name)
    return redirect(request.referrer)


@app.route('/api/delete/data/subcategory/<subcat_id>/row/<row_id>', methods=['POST'])
def delete_subcategory_data(subcat_id, row_id):
    # Here you do what you want with the info received
    api.delete_row_from_subcategory(db, subcat_id, row_id)
    return redirect(request.referrer)

@app.route('/api/delete/data/category/<cat_id>/row/<row_id>', methods=['POST'])
def delete_category_data(cat_id,row_id):
    # Here you do what you want with the info received
    api.delete_row_from_category(db, cat_id, row_id)
    return redirect(request.referrer)

@app. route('/api/delete/data/paper/<paper_id>', methods=['POST'])
def delete_paper_data(paper_id):
    api.delete_paper_by_id(db, paper_id)
    return redirect(request.referrer)

@app.route('/api/add/data/category/<cat_id>/subcategory/<subcat_id>', methods=['POST'])
def add_data_to_subcat(cat_id,subcat_id):
    category_properties = api.get_all_properties_from_category_as_dict_array(db, cat_id)
    category_properties = api.remove_subcategories_duplicated(category_properties)
    dict_array = []
    for prop in category_properties:
        # request.form is a dictionary with the form stuff
        if prop['type'] == 'subcat':
            if str(prop['id']) == str(subcat_id):
                for element in prop['properties']:
                    form_field = "sub-"+subcat_id+"-cat-"+cat_id+"-"+element
                    value = request.form.get(form_field)
                    dict_array.append({'id_name':element,
                                       element:value})
    api.add_data_row_to_subcategory(db,subcat_id,dict_array)
    return redirect(request.referrer)


@app.route('/api/add/data/category/<cat_id>', methods=['POST'])
def add_data_to_cat(cat_id):
    category_properties = api.get_all_properties_from_category_as_dict_array(db, cat_id)
    dict_array = []
    for prop in category_properties:
        prop_name = prop['name'].replace(" ","-")
        # request.form is a dictionary with the form stuff
        if prop['type'] == 'subcat':
            name = (prop['interaction']+prop['name']).replace(" ","_")
            form_field = "sub-"+name+"-cat-"+cat_id
            dict_array.append({'id_name':prop_name,
                               prop_name: request.form.getlist(form_field),
                               'rel_with_cat':prop['interaction'],
                               'is_subcat':True,
                               'id':prop['id']})
        else:
            form_field = "sub-"+prop['name']+"-cat-"+cat_id
            dict_array.append({'id_name':prop_name,
                               prop_name: request.form.get(form_field),
                               'is_subcat':False})
    api.add_data_row_to_category(db,cat_id,dict_array)
    return redirect(request.referrer)


@app.route('/api/request/headers/category/<cat_id>')
def request_headers_from_cat(cat_id):
    full_data = api.get_data_from_category_as_headers_and_column_data(db, cat_id)
    headers = full_data['headers']
    cat_name = api.get_category_name_from_id(db, cat_id)
    return jsonify(headers=headers, name=cat_name)

@app.route('/api/request/data/category/<cat_id>')
def request_data_from_cat(cat_id):
    full_data = api.get_data_from_category_as_headers_and_column_data(db, cat_id)
    headers = full_data['headers']
    data = full_data['rows']
    return jsonify(column_headers=headers, column_data=data)

@app.route('/api/request/data/subcategory/<subcat_id>')
def request_data_from_subcat(subcat_id):
    full_data = api.get_data_from_subcategory_as_headers_and_column_data(db, subcat_id)
    headers = full_data['headers']
    data = full_data['rows']
    return jsonify(column_headers=headers, column_data=data)


@app.route('/api/request/data/paper/<paper_id>/')
def get_paper_info_and_values(paper_id):
    paper_properties = api.get_paper_properties_and_values(db, paper_id)
    return jsonify(properties=paper_properties)




@app.route('/api/request/headers/paper/')
def get_paper_info():
    paper_properties = api.get_paper_properties(db)
    return jsonify(properties=paper_properties)



@app.route('/api/edit/category/<cat_id>/row/<row_id>', methods=['POST'])
def edit_data_from_category(cat_id,row_id):
    category_properties = api.get_all_properties_from_category_as_dict_array(db, cat_id)
    dict_array = []
    for prop in category_properties:
        prop_name = prop['name'].replace(" ","-")
        if prop_name == 'id':
            continue
        # request.form is a dictionary with the form stuff
        if prop['type'] == 'subcat':
            form_field = "sub-"+(prop['interaction']).replace("_","-")+"-"+(prop['name']).replace(" ","-")+"-cat-"+cat_id
            dict_array.append({'id_name':prop_name,
                               prop_name: request.form.getlist(form_field),
                               'rel_with_cat':prop['interaction'],
                               'is_subcat':True,
                               'id':prop['id']})
        else:
            form_field = "sub-"+prop['name']+"-cat-"+cat_id
            print(form_field)
            print(request.form.get(form_field))
            dict_array.append({'id_name':prop_name,
                               prop_name: request.form.get(form_field),
                               'is_subcat':False})
    api.edit_data_row_to_category(db, cat_id, row_id, dict_array)
    return redirect(request.referrer)

@app.route('/api/edit/category/<cat_id>/subcategory/<subcat_id>/row/<row_id>', methods=['POST'])
def edit_data_from_subcategory(cat_id,subcat_id,row_id):
    category_properties =api.get_all_properties_from_category_as_dict_array(db, cat_id)
    dict_array = []
    for prop in category_properties:
        # request.form is a dictionary with the form stuff
        if prop['type'] == 'subcat':
            if str(prop['id']) == str(subcat_id):
                for element in prop['properties']:
                    form_field = "sub-"+subcat_id+"-cat-"+cat_id+"-"+element
                    value = request.form.get(form_field)
                    dict_array.append({'id_name':element,
                                       element:value})
    api.edit_data_row_to_subcategory(db,subcat_id,row_id,dict_array)
    return redirect(request.referrer)

@app.route('/api/edit/data/paper/<paper_id>/', methods=['POST'])
def edit_data_from_paper(paper_id):
    paper_properties = api.get_paper_properties(db)
    dict_array = []
    for prop in paper_properties:
        prop_name = prop['name'].replace(" ","-")
        form_field = "paper-"+paper_id+"-"+prop_name
        # request.form is a dictionary with the form stuff
        if prop['type'] == 'category':
            dict_array.append({'name':prop_name,
                               prop_name: request.form.getlist(form_field)})
        else:
            dict_array.append({'name':prop_name,
                               prop_name: request.form.get(form_field)})
    api.edit_paper_using_dict_array(db, paper_id,dict_array)
    return redirect(request.referrer)


@app.route('/api/add/paper/', methods=['POST'])
def add_paper():
    paper_properties = api.get_paper_properties(db)
    dict_array = []
    for prop in paper_properties:
        prop_name = prop['name'].replace(" ","-")
        form_field = "paper-"+prop_name
        # request.form is a dictionary with the form stuff
        if prop['type'] == 'category':
            dict_array.append({'name':prop_name,
                               prop_name: request.form.getlist(form_field)})
        else:
            dict_array.append({'name':prop_name,
                               prop_name: request.form.get(form_field)})
    api.add_paper_using_dict_array(db, dict_array)

    return redirect(request.referrer)


@app.route('/api/add/author/', methods=['POST'])
def add_author():
    author_name = request.form.get("author-name")
    author_affiliation = request.form.get("author-affiliation")
    api.add_author(db, author_name, author_affiliation)
    return redirect(request.referrer)


@app.route('/api/edit/data/author/<author_id>', methods=['POST'])
def modify_author(author_id):
    author_name = request.form.get("author-name")
    author_affiliation = request.form.get("author-affiliation")
    api.modify_author(db, author_id, author_name, author_affiliation)
    return redirect(request.referrer)


@app.route('/api/request/data/author/')
def get_authors():
    full_data = api.get_data_from_authors_as_headers_and_column_data(db)
    headers = full_data['headers']
    data = full_data['rows']
    return jsonify(column_headers=headers, column_data=data)

@app.route('/api/delete/data/author/<author_id>', methods=['POST'])
def delete_author(author_id):
    api.delete_author(db, author_id)
    return redirect(request.referrer)
