from app import app, db
from flask import render_template
from flask import request
import api.db_api as db_api
import operator


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

@app.route('/visual')
def visual():
    return render_template('visual.html')

@app.route('/visual/<category>/<visualization_name>/<all_or_year>')
def visual_2(category, visualization_name, all_or_year):

    bar_visualization = False
    pie_visualization = False
    line_visualization = False
    visualize_all = False
    visualize_year = False

    if all_or_year == "all":
        visualize_all = True
        values = amount_of_papers(category)
    elif all_or_year == "year":
        visualize_year = True
        values = amount_of_papers_per_year(category)

    if visualization_name == "bar":
        bar_visualization = True
    elif visualization_name == "pie":
        pie_visualization = True
    elif visualization_name == "line":
        line_visualization = True
    print values
    return render_template('visual.html',
                           category=category,
                           dict=values,
                           bar_visualization=bar_visualization,
                           pie_visualization=pie_visualization,
                           line_visualization=line_visualization,
                           visualization_name=visualization_name,
                           visualize_all=visualize_all,
                           visualize_year=visualize_year)


def amount_of_papers_per_year(category):
    dict_amount_per_year = {}
    for year in range(2005,2018):
        dict_amount_per_year[year] = amount_of_papers(category,specific_year=year)
    return dict_amount_per_year


def amount_of_papers(category, specific_year=0):
    print_all = False
    dict_amount_per_category = {}
    cat_id = ''
    subcat_id = ''
    is_cat = False
    is_subcat = False
    is_time = False
    if category == 'model':
        is_subcat = True
        is_cat = False
        value_selected = "model type"
        subcat_id = db_api.get_subcategory_id_from_name(db,value_selected)
    elif category == 'metric':
        is_subcat = True
        is_cat = False
        value_selected = "type"
        subcat_id = db_api.get_subcategory_id_from_name(db,value_selected)
    elif category in ['network_tested','study']:
        is_subcat = False
        is_cat = True
        value_selected = category.replace("_"," ")
        cat_id = db_api.get_category_id_from_name(db,value_selected)
    elif category == "time" and specific_year in range(2005,2017):
        is_time = True

    year = ''
    if specific_year in range(2005, 2018):
        year = str(specific_year)
    paper_properties = db_api.get_paper_properties(db)

    rows = []
    if is_subcat:
        rows = db_api.get_subcategory_data(db,subcat_id)
    elif is_cat:
        rows = db_api.get_data_from_category_by_cat_id(db,cat_id)

    if category == "study" and not print_all:
        studies_white_list = ['Percolation','Coupling','Targeted attacks','Size of the giant connected component','Load and capacity','Avalanche','Cascading time','Length']
        aux_list = []
        for element in rows:
            if element['name'] in studies_white_list:
                aux_dict = {'name':element['name'],'id':element['id']}
                aux_list.append(aux_dict)
        rows = aux_list

    if category == "model":
        models_black_list = ['antagonistic-dependent','state dependent']
        aux_list = []
        for element in rows:
            if not element['name'] in models_black_list:
                aux_dict = {'name':element['name'],'id':element['id']}
                aux_list.append(aux_dict)
        rows = aux_list

    if is_time:
        rows = [1]

    for row_item in rows:
        # values maintains the previous field values on the search form
        values = {}
        paper_values = []
        authors_value = ""
        categories_values = []
        for prop in paper_properties:
            if not prop['type'] == 'category':
                if prop['name'] == 'authors':
                    #authors_value = '' ##### MIRAR ESTA PARTE
                    values[prop['name']] = '' ##### MIRAR ESTA PARTE
                elif prop['name'] == 'year':
                    paper_values.append({'id_name':(prop['name']).replace(" ","_"),
                                         'value':year})##### MIRAR ESTA PARTE
                    values[prop['name']] = year##### MIRAR ESTA PARTE
                else:
                    paper_values.append({'id_name':(prop['name']).replace(" ","_"),
                                         'value':''})##### MIRAR ESTA PARTE
                    values[prop['name']] = ''##### MIRAR ESTA PARTE
            else:
                category_values = []
                full_data = db_api.get_data_from_category_as_headers_and_column_data(db, prop['id'])
                cat_prop = full_data['headers']

                for c_prop in cat_prop:

                    if c_prop['name'] == 'id':
                        continue
                    if c_prop['type'] == 'subcat':
                        value = ''##### MIRAR ESTA PARTE

                        if is_subcat and c_prop['id'] == subcat_id:
                            value = row_item['name']
                        category_values.append({'subcat_id':c_prop['id'],
                                                'rel_with_cat':c_prop['rel_with_cat'],
                                                'name_value':value,
                                                'is_subcat':True})

                        values[prop['name']+c_prop['name']] = value
                    else:
                        value = ''##### MIRAR ESTA PARTE
                        if is_cat and prop['id'] == cat_id and c_prop['name'] == "name":
                            value = row_item['name']
                        category_values.append({'id_name':(c_prop['name']).replace(" ","_"),
                                                'value':value,
                                                'is_subcat':False})
                        values[prop['name']+c_prop['name']] = value

                categories_values.append({'cat_id':prop['id'],'values':category_values})
        paper_ids = db_api.search_papers_id(db, paper_values, authors_value, categories_values)

        if not is_time:
            dict_amount_per_category[row_item['name']] = len(paper_ids)
        else:
            return len(paper_ids)

    if category=="study" and print_all:
        counter = 0
        for w in sorted(dict_amount_per_category, key=dict_amount_per_category.get, reverse=True):

            if dict_amount_per_category[w] > 0:
                print "'",w,"',"#dict_amount_per_category[w]
                counter += 1
        print "Total de estudios: ",counter

    return dict_amount_per_category

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
                    values[prop['name']] = request.form.get(field_name) ##### MIRAR ESTA PARTE
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
        # here the search is performed and then we render the template again

        paper_ids = db_api.search_papers_id(db, paper_values, authors_value, categories_values)
        paper_aux =[]
        aps_aux = [225, 380, 50, 87, 374, 324, 325, 328, 384, 534, 535, 533, 532, 542, 376, 369, 536, 537, 538, 539, 540, 541]
        for papers in paper_ids:
            if papers not in aps_aux:
                paper_aux.append(int(papers))
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




