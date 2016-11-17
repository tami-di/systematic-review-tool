from app import app, db
from flask import jsonify
from flask import request
from flask import redirect
import db_api


@app.route('/api/category/<cat_id>/subcategories')
def subcategories(cat_id):
    subcats = db_api.get_all_properties_from_category_as_dict_array(db, cat_id)
    return jsonify(subcategories=subcats)


def remove_subcategories_duplicated(dict_array_subcategories):
    dict_array = []
    subcat_ids_added = []
    for element in dict_array_subcategories:
        if element['is_subcat']:
            if element['id'] not in subcat_ids_added:
                subcat_ids_added.append(element['id'])
                dict_array.append(element)
        else:
            dict_array.append(element)
    return dict_array

@app.route('/api/category/<cat_id>/subcategories/without_inter/')
def subcategories_without_interaction(cat_id):
    subcats = db_api.get_all_properties_from_category_as_dict_array(db, cat_id)
    dict_array = remove_subcategories_duplicated(subcats)
    return jsonify(subcategories=dict_array)

@app.route('/api/subcategory_data/<subcat_id>')
def subcategory_data(subcat_id):
    subcats_data = db_api.get_subcategory_data(db, subcat_id)
    # subcats_data = [{'name': 'Fluff','id': 1},{'name': 'Spoofi','id': 2},
    #            {'name': 'dato 3','id': 3},{'name': 'dato 4','id': 4},
    #            {'name': 'dato 5','id': 5}]

    return jsonify(subcategory_data=subcats_data)


def category_data_aux(cat_id):
    cats_data = [{'name': 'cucurilo','id': 1},{'name': 'Snuffles','id': 2},
               {'name': 'CuackCuack','id': 3}]
    return cats_data

@app.route('/api/category_data/<cat_id>')
def category_data(cat_id):
    return jsonify(category_data=category_data_aux(cat_id))


@app.route('/api/add_subcategory', methods=['POST'])
def add_subcategory():
    # request.form is a dictionary with the form stuff
    select_existig_subcat_id = request.form.get('select-existig-subcat')
    subcat_name = request.form.get('subcat-name')
    category_of_subcategory_id = int(request.form.get('category-of-subcategory'))
    cat_interaction_with_subcat = (str(request.form.get('cat-interaction-with-subcat'))).replace(" ","_")
    # Here you do what you want with the info received
    if select_existig_subcat_id == str(0):
        db_api.create_subcategory(db,subcat_name,category_of_subcategory_id,cat_interaction_with_subcat)
    else:
        db_api.create_interaction_for_existing_subcategory(db,category_of_subcategory_id,cat_interaction_with_subcat,
                                                           select_existig_subcat_id)
    return redirect(request.referrer)


@app.route('/api/request_data/subcategories/category/<cat_id>')
def get_subcategories_name_and_if_from_category(cat_id):
    subcats_ids = db_api.get_all_subcategories_id_of_category_as_array(db, cat_id)
    dict_array = []
    for subcat_id in subcats_ids:
        subcat_name = db_api.get_subcategory_name_from_id(db,subcat_id)
        dict_array.append({'subcat_id':subcat_id,'subcat_name':subcat_name})
    # request.form is a dictionary with the form stuff
    return jsonify(subcategories_info=dict_array )


@app.route('/api/add_category', methods=['POST'])
def add_category():
    # request.form is a dictionary with the form stuff
    cat_name = request.form.get('cat-name')
    cat_description = request.form.get('cat-description')
    # Here you do what you want with the info received
    db_api.create_category(db, cat_name, cat_description)
    return redirect(request.referrer)

@app.route('/api/add_column/<cat_id>/category', methods=['POST'])
def add_column_to_category(cat_id):
    # request.form is a dictionary with the form stuff
    col_name = request.form.get('col-name')
    col_data = request.form.get('select-data-type')
    # Here you do what you want with the info received
    db_api.add_column_to_category(db, cat_id, col_name, col_data)
    return redirect(request.referrer)

@app.route('/api/add_column/<subcat_id>/subcategory', methods=['POST'])
def add_column_to_subcategory(subcat_id):
    # request.form is a dictionary with the form stuff
    col_name = request.form.get('col-name')
    col_data = request.form.get('select-data-type')
    # Here you do what you want with the info received
    db_api.add_column_to_subcategory(db, subcat_id, col_name, col_data)
    return redirect(request.referrer)


@app.route('/api/delete_element', methods=['POST'])
def delete_element():
    # request.form is a dictionary with the form stuff
    delete_element_btn = request.form.get('delete-element-btn')
    deleted_element = request.form.get('deleted-element')
    # Here you do what you want with the info received
    return redirect(request.referrer)


@app.route('/api/delete_category/<cat_id>', methods=['POST'])
def delete_category(cat_id):
    # Here you do what you want with the info received
    db_api.delete_category_by_id(db,cat_id)
    return redirect(request.referrer)


@app.route('/api/delete_subcategory/<subcat_id>/category/<cat_id>', methods=['POST'])
def delete_subcategory(subcat_id,cat_id):
    # Here you do what you want with the info received
    db_api.delete_subcategory_by_id(db, subcat_id,cat_id=cat_id)
    return redirect(request.referrer)


@app.route('/api/delete_column/<column_name>/category/<cat_id>', methods=['POST'])
def delete_category_column(cat_id,column_name):
    # Here you do what you want with the info received
    db_api.delete_category_column(db, cat_id,column_name)
    return redirect(request.referrer)


@app.route('/api/delete_data/subcategory/<subcat_id>/row/<row_id>', methods=['POST'])
def delete_subcategory_data(subcat_id, row_id):
    # Here you do what you want with the info received
    db_api.delete_row_from_subcategory(db, subcat_id, row_id)
    return redirect(request.referrer)

@app.route('/api/delete_data/category/<cat_id>/row/<row_id>', methods=['POST'])
def delete_category_data(cat_id,row_id):
    # Here you do what you want with the info received
    db_api.delete_row_from_category(db, cat_id, row_id)
    return redirect(request.referrer)


@app.route('/api/add_data/category/<cat_id>/subcategory/<subcat_id>', methods=['POST'])
def add_data_to_subcat(cat_id,subcat_id):
    category_properties = db_api.get_all_properties_from_category_as_dict_array(db, cat_id)
    category_properties = remove_subcategories_duplicated(category_properties)
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
    db_api.add_data_row_to_subcategory(db,subcat_id,dict_array)
    return redirect(request.referrer)


@app.route('/api/add_data/category/<cat_id>', methods=['POST'])
def add_data_to_cat(cat_id):
    category_properties = db_api.get_all_properties_from_category_as_dict_array(db, cat_id)
    dict_array = []
    for prop in category_properties:
        prop_name = prop['name'].replace(" ","-")
        # request.form is a dictionary with the form stuff
        if prop['type'] == 'subcat':
            form_field = "sub-"+prop['interaction']+prop['name']+"-cat-"+cat_id
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
    db_api.add_data_row_to_category(db,cat_id,dict_array)
    return redirect(request.referrer)



def request_headers_from_cat_aux(cat_id):
    headers = [{'name': 'subcategoria 1',
                'id': 1,
                'properties': ['name','description','patitos'],
                'properties_type':{'name':'varchar','description':'text','patitos':'number'},
                'type':'subcat',
                'is_subcat':True},
               {'name': 'propiedad 2',
                'id': 2,
                'properties': [],
                'type':'varchar',
                'is_subcat':False},
               {'name': 'propiedad 3',
                'id': 3,
                'properties': [],
                'type':'number',
                'is_subcat':False},
               {'name': 'propiedad 4',
                'id': 4,
                'type':'text',
                'properties': [],
                'is_subcat':False}]
    return headers


@app.route('/api/request_headers/category/<cat_id>')
def request_headers_from_cat(cat_id):
    full_data = db_api.get_data_from_category_as_headers_and_column_data(db, cat_id)
    headers = full_data['headers']
    cat_name = db_api.get_category_name_from_id(db, cat_id)
    return jsonify(headers=headers, name=cat_name)

@app.route('/api/request_data/category/<cat_id>')
def request_data_from_cat(cat_id):
    full_data = db_api.get_data_from_category_as_headers_and_column_data(db, cat_id)
    headers = full_data['headers']
    data = full_data['rows']
    # headers = request_headers_from_cat_aux(cat_id)
    # data_row_1 = {'subcategoria 1':'Fluff',
    #               'propiedad 2':'patiters',
    #               'propiedad 3':'3',
    #               'propiedad 4':'Los patitos son extra fluferinos'}
    # data_row_2 = {'subcategoria 1':'Spoofi',
    #               'propiedad 2':'Cuack',
    #               'propiedad 3':'8',
    #               'propiedad 4':'Gatinis que hacen pancitos'}
    # data = [data_row_1,data_row_2]
    return jsonify(column_headers=headers, column_data=data)

@app.route('/api/request_data/subcategory/<subcat_id>')
def request_data_from_subcat(subcat_id):
    full_data = db_api.get_data_from_subategory_as_headers_and_column_data(db, subcat_id)
    headers = full_data['headers']
    data = full_data['rows']
    # headers = [{'name':'name','type':'varchar'},
    #            {'name':'description','type':'text'},
    #            {'name':'patitos','type':'number'}]
    #
    # data_row_1 = {'name':'Kiwi',
    #               'description':'Es un pajarito redondito',
    #               'patitos':'10'}
    # data_row_2 = {'name':'Hamster',
    #               'description':'Es un ratoncito redondito y feroz',
    #               'patitos':'3'}
    # data_row_3 = {'name':'Round Robin',
    #               'description':'Es un Robin (pajarito) redondito',
    #               'patitos':'1'}
    # data = [data_row_1,data_row_2,data_row_3]
    return jsonify(column_headers=headers, column_data=data)




@app.route('/api/request_data/paper/<paper_id>/')
def get_paper_info_and_values(paper_id):
    # cat_data = category_data_aux(1)
    # paper_properties = [{'name':'title','type':'varchar','value':'El paper 1'},
    #                     {'name':'authors','type':'varchar','value':'autor 1; autor 2; autor 3'},
    #                     {'name':'abstract','type':'text','value':'El paper dice cositas muy choris.'},
    #                     {'name':'summary','type':'text','value':'El paper dice cositas como cuackers y miau.'},
    #                     {'name':'categoria 1','type':'category','value':'Snuffles','data':cat_data,"id":1}]
    paper_properties = db_api.get_paper_properties_and_values(db, paper_id)
    return jsonify(properties=paper_properties)


@app.route('/api/request_data/paper/')
def get_paper_info():
    # cat_data = category_data_aux(1)
    # paper_properties = [{'name':'title','type':'varchar','value':'El paper 1'},
    #                     {'name':'authors','type':'varchar','value':'autor 1; autor 2; autor 3'},
    #                     {'name':'abstract','type':'text','value':'El paper dice cositas muy choris.'},
    #                     {'name':'summary','type':'text','value':'El paper dice cositas como cuackers y miau.'},
    #                     {'name':'categoria 1','type':'category','value':'Snuffles','data':cat_data,"id":1}]
    paper_properties = db_api.get_paper_properties(db)
    return jsonify(properties=paper_properties)


@app.route('/api/edit_data/<cat_id>/category/<row_id>/row', methods=['POST'])
def edit_data_from_category(cat_id,row_id):
    category_properties = db_api.get_all_properties_from_category_as_dict_array(db, cat_id)
    dict_array = []
    for prop in category_properties:
        prop_name = prop['name'].replace(" ","-")
        if prop_name == 'id':
            continue
        # request.form is a dictionary with the form stuff
        if prop['type'] == 'subcat':
            print prop
            form_field = "sub-"+(prop['interaction']).replace("_","-")+"-"+prop['name']+"-cat-"+cat_id
            dict_array.append({'id_name':prop_name,
                               prop_name: request.form.getlist(form_field),
                               'rel_with_cat':prop['interaction'],
                               'is_subcat':True,
                               'id':prop['id']})
            print form_field,":",request.form.getlist(form_field)
        else:
            form_field = "sub-"+prop['name']+"-cat-"+cat_id
            dict_array.append({'id_name':prop_name,
                               prop_name: request.form.get(form_field),
                               'is_subcat':False})
    db_api.edit_data_row_to_category(db, cat_id, row_id, dict_array)
    return redirect(request.referrer)

@app.route('/api/edit_data/<cat_id>/category/<subcat_id>/subcategory/<row_id>/row', methods=['POST'])
def edit_data_from_subcategory(cat_id,subcat_id,row_id):
    category_properties = db_api.get_all_properties_from_category_as_dict_array(db, cat_id)
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
    db_api.edit_data_row_to_subcategory(db,subcat_id,row_id,dict_array)
    return redirect(request.referrer)

@app.route('/api/edit_paper/<paper_id>/', methods=['POST'])
def edit_data_from_paper(paper_id):
    paper_properties = db_api.get_paper_properties(db)
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
    db_api.edit_paper_using_dict_array(db, paper_id,dict_array)
    return redirect(request.referrer)


@app.route('/api/add_paper/', methods=['POST'])
def add_paper():
    paper_properties = db_api.get_paper_properties(db)
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
    db_api.add_paper_using_dict_array(db, dict_array)

    return redirect(request.referrer)


@app.route('/api/add_data/author/', methods=['POST'])
def add_author():
    author_name = request.form.get("author-name")
    author_affiliation = request.form.get("author-affiliation")
    db_api.add_author(db, author_name, author_affiliation)
    return redirect(request.referrer)


@app.route('/api/modify_data/author/<author_id>', methods=['POST'])
def modify_author(author_id):
    author_name = request.form.get("author-name")
    author_affiliation = request.form.get("author-affiliation")
    db_api.modify_author(db, author_id, author_name, author_affiliation)
    return redirect(request.referrer)


@app.route('/api/request_data/author/')
def get_authors():
    full_data = db_api.get_data_from_authors_as_headers_and_column_data(db)
    headers = full_data['headers']
    data = full_data['rows']
    return jsonify(column_headers=headers, column_data=data)

@app.route('/api/delete_data/author/<author_id>', methods=['POST'])
def delete_author(author_id):
    db_api.delete_row_from_author(db, author_id)
    return redirect(request.referrer)