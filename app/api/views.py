from app import app, db
from flask import jsonify
from flask import request
from flask import redirect
import db_api


@app.route('/api/request/headers+subcategories/<cat_id>')
def subcategories(cat_id):
    subcats = db_api.get_all_properties_from_category_as_dict_array(db.connection, cat_id)
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

@app.route('/api/request/headers+subcategories/norep/<cat_id>')
def subcategories_without_interaction(cat_id):
    subcats = db_api.get_all_properties_from_category_as_dict_array(db.connection, cat_id)
    dict_array = remove_subcategories_duplicated(subcats)
    return jsonify(subcategories=dict_array)

@app.route('/api/request/headers/subcategory/<subcat_id>')
def subcategory_data(subcat_id):
    subcats_data = db_api.get_subcategory_data(db.connection, subcat_id)
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
        db_api.create_subcategory(db.connection,subcat_name,category_of_subcategory_id,cat_interaction_with_subcat)
    else:
        db_api.create_interaction_for_existing_subcategory(db.connection,category_of_subcategory_id,cat_interaction_with_subcat,
                                                           select_existig_subcat_id)
    return redirect(request.referrer)


@app.route('/api/request/data/subcategories/category/<cat_id>')
def get_subcategories_name_and_if_from_category(cat_id):
    subcats_ids = db_api.get_all_subcategories_id_of_category_as_array(db.connection, cat_id)
    dict_array = []
    for subcat_id in subcats_ids:
        subcat_name = db_api.get_subcategory_name_from_id(db.connection,subcat_id)
        dict_array.append({'subcat_id':subcat_id,'subcat_name':subcat_name})
    # request.form is a dictionary with the form stuff
    return jsonify(subcategories_info=dict_array )


@app.route('/api/add/category/', methods=['POST'])
def add_category():
    # request.form is a dictionary with the form stuff
    cat_name = request.form.get('cat-name')
    cat_description = request.form.get('cat-description')
    # Here you do what you want with the info received
    db_api.create_category(db.connection, cat_name, cat_description)
    return redirect(request.referrer)

@app.route('/api/add/column/category/<cat_id>', methods=['POST'])
def add_column_to_category(cat_id):
    # request.form is a dictionary with the form stuff
    col_name = request.form.get('col-name')
    col_data = request.form.get('select-data-type')
    # Here you do what you want with the info received
    db_api.add_column_to_category(db.connection, cat_id, col_name, col_data)
    return redirect(request.referrer)

@app.route('/api/add_column/<subcat_id>/subcategory', methods=['POST'])
def add_column_to_subcategory(subcat_id):
    # request.form is a dictionary with the form stuff
    col_name = request.form.get('col-name')
    col_data = request.form.get('select-data-type')
    # Here you do what you want with the info received
    db_api.add_column_to_subcategory(db.connection, subcat_id, col_name, col_data)
    return redirect(request.referrer)


@app.route('/api/delete/category/<cat_id>', methods=['POST'])
def delete_category(cat_id):
    # Here you do what you want with the info received
    db_api.delete_category_by_id(db.connection,cat_id)
    return redirect(request.referrer)


@app.route('/api/delete/subcategory/<subcat_id>/category/<cat_id>', methods=['POST'])
def delete_subcategory(subcat_id,cat_id):
    # Here you do what you want with the info received
    db_api.delete_subcategory_by_id(db.connection, subcat_id,cat_id=cat_id)
    return redirect(request.referrer)


@app.route('/api/delete/column/<column_name>/category/<cat_id>', methods=['POST'])
def delete_category_column(cat_id,column_name):
    # Here you do what you want with the info received
    db_api.delete_category_column(db.connection, cat_id,column_name)
    return redirect(request.referrer)


@app.route('/api/delete/data/subcategory/<subcat_id>/row/<row_id>', methods=['POST'])
def delete_subcategory_data(subcat_id, row_id):
    # Here you do what you want with the info received
    db_api.delete_row_from_subcategory(db.connection, subcat_id, row_id)
    return redirect(request.referrer)

@app.route('/api/delete/data/category/<cat_id>/row/<row_id>', methods=['POST'])
def delete_category_data(cat_id,row_id):
    # Here you do what you want with the info received
    db_api.delete_row_from_category(db.connection, cat_id, row_id)
    return redirect(request.referrer)


@app.route('/api/add/data/category/<cat_id>/subcategory/<subcat_id>', methods=['POST'])
def add_data_to_subcat(cat_id,subcat_id):
    category_properties = db_api.get_all_properties_from_category_as_dict_array(db.connection, cat_id)
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
    db_api.add_data_row_to_subcategory(db.connection,subcat_id,dict_array)
    return redirect(request.referrer)


@app.route('/api/add/data/category/<cat_id>', methods=['POST'])
def add_data_to_cat(cat_id):
    category_properties = db_api.get_all_properties_from_category_as_dict_array(db.connection, cat_id)
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
    db_api.add_data_row_to_category(db.connection,cat_id,dict_array)
    return redirect(request.referrer)


@app.route('/api/request/headers/category/<cat_id>')
def request_headers_from_cat(cat_id):
    full_data = db_api.get_data_from_category_as_headers_and_column_data(db.connection, cat_id)
    headers = full_data['headers']
    cat_name = db_api.get_category_name_from_id(db.connection, cat_id)
    return jsonify(headers=headers, name=cat_name)

@app.route('/api/request/data/category/<cat_id>')
def request_data_from_cat(cat_id):
    full_data = db_api.get_data_from_category_as_headers_and_column_data(db.connection, cat_id)
    headers = full_data['headers']
    data = full_data['rows']
    return jsonify(column_headers=headers, column_data=data)

@app.route('/api/request/data/subcategory/<subcat_id>')
def request_data_from_subcat(subcat_id):
    full_data = db_api.get_data_from_subategory_as_headers_and_column_data(db.connection, subcat_id)
    headers = full_data['headers']
    data = full_data['rows']
    return jsonify(column_headers=headers, column_data=data)


@app.route('/api/request/data/paper/<paper_id>/')
def get_paper_info_and_values(paper_id):
    paper_properties = db_api.get_paper_properties_and_values(db.connection, paper_id)
    return jsonify(properties=paper_properties)


@app.route('/api/request/headers/paper/')
def get_paper_info():
    paper_properties = db_api.get_paper_properties(db.connection)
    return jsonify(properties=paper_properties)


@app.route('/api/edit/category/<cat_id>/row/<row_id>', methods=['POST'])
def edit_data_from_category(cat_id,row_id):
    category_properties = db_api.get_all_properties_from_category_as_dict_array(db.connection, cat_id)
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
            dict_array.append({'id_name':prop_name,
                               prop_name: request.form.get(form_field),
                               'is_subcat':False})
    db_api.edit_data_row_to_category(db.connection, cat_id, row_id, dict_array)
    return redirect(request.referrer)

@app.route('/api/edit/category/<cat_id>/subcategory/<subcat_id>/row/<row_id>', methods=['POST'])
def edit_data_from_subcategory(cat_id,subcat_id,row_id):
    category_properties = db_api.get_all_properties_from_category_as_dict_array(db.connection, cat_id)
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
    db_api.edit_data_row_to_subcategory(db.connection,subcat_id,row_id,dict_array)
    return redirect(request.referrer)

@app.route('/api/edit/data/paper/<paper_id>/', methods=['POST'])
def edit_data_from_paper(paper_id):
    paper_properties = db_api.get_paper_properties(db.connection)
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
    db_api.edit_paper_using_dict_array(db.connection, paper_id,dict_array)
    return redirect(request.referrer)


@app.route('/api/add/paper/', methods=['POST'])
def add_paper():
    paper_properties = db_api.get_paper_properties(db.connection)
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
    db_api.add_paper_using_dict_array(db.connection, dict_array)

    return redirect(request.referrer)


@app.route('/api/add/author/', methods=['POST'])
def add_author():
    author_name = request.form.get("author-name")
    author_affiliation = request.form.get("author-affiliation")
    db_api.add_author(db.connection, author_name, author_affiliation)
    return redirect(request.referrer)


@app.route('/api/edit/data/author/<author_id>', methods=['POST'])
def modify_author(author_id):
    author_name = request.form.get("author-name")
    author_affiliation = request.form.get("author-affiliation")
    db_api.modify_author(db.connection, author_id, author_name, author_affiliation)
    return redirect(request.referrer)


@app.route('/api/request/data/author/')
def get_authors():
    full_data = db_api.get_data_from_authors_as_headers_and_column_data(db.connection)
    headers = full_data['headers']
    data = full_data['rows']
    return jsonify(column_headers=headers, column_data=data)

@app.route('/api/delete/data/author/<author_id>', methods=['POST'])
def delete_author(author_id):
    db_api.delete_row_from_author(db.connection, author_id)
    return redirect(request.referrer)
    