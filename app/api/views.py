from app import app
from flask import jsonify
from flask import request
from flask import redirect

@app.route('/api/category/<id>/subcategories')
def subcategories(id):
    subcats = [{'name': 'subcategoria 1',
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
    return jsonify(subcategories=subcats)


@app.route('/api/category/<id_cat>/subcategory_data/<id>')
def subcategory_data(id_cat,id):
    subcats_data = [{'name': 'Fluff','id': 1},{'name': 'Spoofi','id': 2},
               {'name': 'dato 3','id': 3},{'name': 'dato 4','id': 4},
               {'name': 'dato 5','id': 5}]

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
    subcat_name = request.form.get('subcat-name')
    category_of_subcategory = request.form.get('category-of-subcategory')
    cat_interaction_with_subcat = request.form.get('cat-interaction-with-subcat')
    # Here you do what you want with the info received
    print subcat_name, category_of_subcategory, cat_interaction_with_subcat
    return redirect(request.referrer)



@app.route('/api/add_category', methods=['POST'])
def add_category():
    # request.form is a dictionary with the form stuff
    cat_name = request.form.get('cat-name')
    cat_description = request.form.get('cat-description')
    # Here you do what you want with the info received
    print cat_name, cat_description
    return redirect(request.referrer)


@app.route('/api/delete_element', methods=['POST'])
def delete_element():
    # request.form is a dictionary with the form stuff
    delete_element_btn = request.form.get('delete-element-btn')
    deleted_element = request.form.get('deleted-element')
    # Here you do what you want with the info received
    print delete_element_btn, deleted_element
    return redirect(request.referrer)

@app.route('/api/delete_data/category/<cat_id>/subcategory/<subcat_id>/row/<row_id>', methods=['POST'])
def delete_subcategory_data(cat_id,subcat_id,row_id):
    # Here you do what you want with the info received
    print cat_id,subcat_id,row_id
    return redirect(request.referrer)

@app.route('/api/delete_data/category/<cat_id>/row/<row_id>', methods=['POST'])
def delete_category_data(cat_id,row_id):
    # Here you do what you want with the info received
    print cat_id,row_id
    return redirect(request.referrer)


@app.route('/api/add_data/category/<cat_id>/subcategory/<subcat_id>', methods=['POST'])
def add_data_to_subcat(cat_id,subcat_id):
    el_name = request.form.get("sub-"+subcat_id+"-cat-"+cat_id+"-"+"name")
    el_description = request.form.get("sub-"+subcat_id+"-cat-"+cat_id+"-"+"description")
    el_patitos = request.form.get("sub-"+subcat_id+"-cat-"+cat_id+"-"+"patitos")
    print "Categoria "+cat_id+"."+subcat_id," : "+el_name, el_description, el_patitos
    return redirect(request.referrer)


@app.route('/api/add_data/category/<cat_id>', methods=['POST'])
def add_data_to_cat(cat_id):
    el_1 = request.form.get('sub-' + str(1) + '-cat-' + cat_id)
    el_2 = request.form.get('sub-' + str(2) + '-cat-' + cat_id)
    el_3 = request.form.get('sub-' + str(3) + '-cat-' + cat_id)
    el_4 = request.form.get('sub-' + str(4) + '-cat-' + cat_id)
    print "Categoria "+cat_id, " : "+ el_1, el_2, el_3, el_4
    return redirect(request.referrer)

@app.route('/api/request_data/category/<cat_id>')
def request_data_from_cat(cat_id):
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
    data_row_1 = {'subcategoria 1':'Fluff',
                  'propiedad 2':'patiters',
                  'propiedad 3':'3',
                  'propiedad 4':'Los patitos son extra fluferinos'}
    data_row_2 = {'subcategoria 1':'Spoofi',
                  'propiedad 2':'Cuack',
                  'propiedad 3':'8',
                  'propiedad 4':'Gatinis que hacen pancitos'}
    data = [data_row_1,data_row_2]
    return jsonify(column_headers=headers, column_data=data)

@app.route('/api/request_data/category/<cat_id>/subcategory/<subcat_id>')
def request_data_from_subcat(cat_id,subcat_id):
    headers = [{'name':'name','type':'varchar'},
               {'name':'description','type':'text'},
               {'name':'patitos','type':'number'}]

    data_row_1 = {'name':'Kiwi',
                  'description':'Es un pajarito redondito',
                  'patitos':'10'}
    data_row_2 = {'name':'Hamster',
                  'description':'Es un ratoncito redondito y feroz',
                  'patitos':'3'}
    data_row_3 = {'name':'Round Robin',
                  'description':'Es un Robin (pajarito) redondito',
                  'patitos':'1'}
    data = [data_row_1,data_row_2,data_row_3]
    return jsonify(column_headers=headers, column_data=data)


@app.route('/api/request_data/paper/<paper_id>/')
def get_paper_info(paper_id):
    cat_data = category_data_aux(1)
    paper_properties = [{'name':'title','type':'varchar','value':'El paper 1'},
                        {'name':'authors','type':'varchar','value':'autor 1; autor 2; autor 3'},
                        {'name':'abstract','type':'text','value':'El paper dice cositas muy choris.'},
                        {'name':'summary','type':'text','value':'El paper dice cositas como cuackers y miau.'},
                        {'name':'categoria 1','type':'category','value':'Snuffles','data':cat_data}]

    return jsonify(properties=paper_properties)


@app.route('/api/edit_data/<cat_id>/category/<row_id>/row', methods=['POST'])
def edit_data_from_category(cat_id,row_id):
    # request.form is a dictionary with the form stuff
    print cat_id, row_id
    cat_name = request.form.get('sub-2-cat-'+cat_id)
    print cat_name
    return redirect(request.referrer)

@app.route('/api/edit_data/<cat_id>/category/<subcat_id>/subcategory/<row_id>/row', methods=['POST'])
def edit_data_from_subcategory(cat_id,subcat_id,row_id):
    # request.form is a dictionary with the form stuff
    print "Category: "+cat_id,"Subcategory: "+subcat_id,"Row: "+ row_id
    cat_name = request.form.get('sub-'+subcat_id+'-cat-'+cat_id+'-name')
    print cat_name
    return redirect(request.referrer)

@app.route('/api/edit_paper/<paper_id>/', methods=['POST'])
def edit_data_from_paper(paper_id):
    # request.form is a dictionary with the form stuff
    cat_name = request.form.get("paper-"+paper_id+"-authors")
    print cat_name
    return redirect(request.referrer)

@app.route('/api/add_paper/<dummy_id>/', methods=['POST'])
def add_paper(dummy_id):
    # request.form is a dictionary with the form stuff
    cat_name = request.form.get("paper-"+dummy_id+"-authors")
    print cat_name
    return redirect(request.referrer)

