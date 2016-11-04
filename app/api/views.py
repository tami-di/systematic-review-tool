from app import app
from flask import jsonify
from flask import request
from flask import redirect

@app.route('/api/category/<id>/subcategories')
def subcategories(id):
    subcats = [{'name': 'subcategoria 1',
                'id': 1,
                'properties': ['name','description','patitos'],
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
    subcats_data = [{'name': 'dato 1','id': 1},{'name': 'dato 2','id': 2},
               {'name': 'dato 3','id': 3},{'name': 'dato 4','id': 4},
               {'name': 'dato 5','id': 5}]

    return jsonify(subcategory_data=subcats_data)



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
def add_delete_element():
    # request.form is a dictionary with the form stuff
    delete_element_btn = request.form.get('delete-element-btn')
    deleted_element = request.form.get('deleted-element')
    # Here you do what you want with the info received
    print delete_element_btn, deleted_element
    return redirect(request.referrer)