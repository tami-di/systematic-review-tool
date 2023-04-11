__author__ = 'ivana'
import re
import db_connection as con

#-------------------------Funciones para Index---------------------------

#-----Agregar paper-----
def get_paper_properties(db):
    cursor = db.connection.cursor()
    dict_array = []
    # get columns
    cursor.execute("show columns from paper")
    for row in cursor.fetchall():
        if row[0] == 'id':
            continue
        # - append name
        # - append type
        if str(row[0]) == 'library':
            dict_array.append({'name':'authors','type':'text'})
        dict_array.append({'name':str(row[0]).replace("_"," "), 'type':parse_type(row[1])})
    # get categories
    cursor.execute("select id, name from categories")
    for row in cursor.fetchall():
        # - get categories data
        data = get_data_from_category_by_cat_id(db, row[0])
        # - append name
        # - append type
        # - append data to category
        dict_array.append({'name':row[1],'type':'category','data':data,'id':row[0]})
    return dict_array


def parse_type(type_name):
    if 'int' in type_name:
        return 'number'
    if 'varchar' in type_name:
        return 'varchar'
    if 'text' in type_name:
        return 'text'
    else:
        return 'varchar'


def get_data_from_category_by_cat_id(db, cat_id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT id, name FROM content WHERE id IN (SELECT cont_id FROM cat_cont WHERE cat_id="+str(cat_id)+")")
    dict_array = []
    for row in cursor.fetchall():
        dict_array.append({'name':row[1],'id':row[0]})
    return dict_array


def get_all_categories_as_dict_array(db):
    cursor = db.connection.cursor()
    cursor.execute("SELECT id, name FROM categories")
    category_dict_array = []
    for row in cursor.fetchall():
        category_dict_array.append({'id':row[0],'name':row[1]})
    return category_dict_array


#-----Buscador-----
def get_paper_id_where_title_exactly(db, title):
    cursor = db.connection.cursor()
    cursor.execute("select id from paper where title=%s",[title])
    for row in cursor.fetchall():
        return row[0]


def get_paper_properties_and_values(db, paper_id):
    dict_array = get_paper_properties(db)
    for dictionary in dict_array:
        if dictionary['name'] == 'authors':
            value = get_authors_from_paper_id_as_str(db, paper_id)
            dictionary['value'] = value
        elif dictionary['type'] == 'category':
            value = get_value_from_category_where_paper_id(db,paper_id,dictionary['id'])
            dictionary['value'] = value
        else:
            value = get_values_from_paper_as_dict(db, paper_id)
            dictionary['value'] = value[dictionary['name']]
    return dict_array


def get_authors_from_paper_id_as_str(db, paper_id):
    cursor = db.connection.cursor()
    authors_str = ""
    cursor.execute("select author_id from paper_has_authors where paper_id=%s",[paper_id])
    for row in cursor.fetchall():
        authors_str += get_author_name_from_id(db,row[0]) + ";"
    return authors_str


def get_author_name_from_id(db,author_id):
    cursor = db.connection.cursor()
    cursor.execute("select name from author where id=%s",[author_id])
    for row in cursor.fetchall():
        return row[0]


def get_value_from_category_where_paper_id(db,paper_id,cat_id):
    cursor = db.connection.cursor()
    value = []
    cursor.execute("SELECT name FROM content WHERE id IN (select cont_id from paper_has_cont where paper_id =%s and cat_id=%s)", [paper_id, cat_id])
    for row in cursor.fetchall():
        value.append(row[0])
    return value


def get_values_from_paper_as_dict(db, paper_id):
    cursor = db.connection.cursor()
    dict = {}
    cursor.execute("select title, library, code_name, year, abstract, summary, source  from paper where id=%s",[paper_id])
    for row in cursor.fetchall():
        dict['title'] = row[0]
        dict['library'] = row[1]
        dict['code name'] = row[2]
        dict['year'] = row[3]
        dict['abstract'] = row[4]
        dict['summary'] = row[5]
        dict['source'] = row[6]
        break
    return dict


#-----Agregar Paper-----
def add_paper_using_dict_array(db, dict_array):
    cursor = db.connection.cursor()
    title = ""
    library = ""
    code_name = ""
    year = ""
    abstract = ""
    summary = ""
    source = ""
    categories = []
    for dictionary in dict_array:
        if dictionary['name'] == 'title':
            title = dictionary['title']
        elif dictionary['name'] == 'library':
            library = dictionary['library']
        elif dictionary['name'] == 'code-name':
            code_name = dictionary['code-name']
        elif dictionary['name'] == 'source':
            source = dictionary['source']
        elif dictionary['name'] == 'year':
            year = dictionary['year']
        elif dictionary['name'] == 'abstract':
            abstract = dictionary['abstract']
        elif dictionary['name'] == 'summary':
            summary = dictionary['summary']
        elif dictionary['name'] == 'authors':
            authors = set_as_list(dictionary['authors'])
        else:
            cont_id=get_content_id_from_name(db,dictionary['name'])
            cont_id=dictionary[dictionary['name']]
            cat_id=[]
            for id in cont_id:
                cat_id.append(get_category_id_from_id_cont(db,id))
            categories.append({'values':cont_id,'cat_id':cat_id})
    # add paper data
    cursor.execute('''insert into paper (title, library, code_name, year, abstract, summary, source) values
    (%s,%s,%s,%s,%s,%s,%s)''', (title, library, code_name, year, abstract, summary, source))
    # get paper_id
    paper_id = get_paper_id_where_title_exactly(db, title)
    # add authors data
    add_authors_to_paper(db, paper_id, authors)
    # add category data
    add_data_to_categories_from_dict_array(db, categories, paper_id)
    # Commit changes in the database
    db.connection.commit()


def set_as_list(string):
    lst = string.split(";")
    return [ r for r in lst if r != '']


def get_content_id_from_name(db,name):
    cursor = db.connection.cursor()
    cursor.execute("SELECT id FROM content WHERE name = %s", [name])
    category_id = ""
    for row in cursor.fetchall():
        category_id = row[0]
        break
    return category_id


def get_category_id_from_id_cont(db,id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT cat_id FROM cat_cont WHERE cont_id="+id)
    category_id = ""
    for row in cursor.fetchall():
        category_id = row[0]
        break
    return category_id


def add_authors_to_paper(db, paper_id, authors):
    cursor = db.connection.cursor()
    for author in authors:
        id = get_or_create_author_id_from_name(db,author)
        cursor.execute("insert into paper_has_authors (paper_id, author_id) values (%s, %s)", (paper_id,id))
    # Commit changes in the database
    db.connection.commit()


def get_or_create_author_id_from_name(db,author_name):
    cursor = db.connection.cursor()
    cursor.execute("select id from author where name=%s",[author_name])
    r = cursor.fetchone()
    if(r):
        return r[0]
    else:
        cursor.execute("INSERT INTO author (name) values (%s)",[author_name])
        cursor.execute("select id from author where name=%s",[author_name])
        x = cursor.fetchone()
        return x[0]
        

def add_data_to_categories_from_dict_array(db, categories, paper_id):
    cursor = db.connection.cursor()
    for category in categories:
        i=0
        for value in category['values']:
            cursor.execute("INSERT INTO paper_has_cont (paper_id, cat_id, cont_id) VALUES (%s,%s,%s)",(paper_id,category['cat_id'][i],value))
            i+=1


#-----Editar Paper-----
def edit_paper_using_dict_array(db, paper_id,dict_array):
    cursor = db.connection.cursor()
    title = ""
    library = ""
    code_name = ""
    year = ""
    abstract = ""
    summary = ""
    categories = []
    authors = ""
    source = ""
    for dictionary in dict_array:
        if dictionary['name'] == 'title':
            title = dictionary['title']
        elif dictionary['name'] == 'library':
            library = dictionary['library']
        elif dictionary['name'] == 'code-name':
            code_name = dictionary['code-name']
        elif dictionary['name'] == 'year':
            year = dictionary['year']
        elif dictionary['name'] == 'abstract':
            abstract = dictionary['abstract']
        elif dictionary['name'] == 'summary':
            summary = dictionary['summary']
        elif dictionary['name'] == 'source':
            source = dictionary['source']
        elif dictionary['name'] == 'authors':
            authors = set_as_list(dictionary['authors'])
        else:
            cont_id=get_content_id_from_name(db,dictionary['name'])
            cont_id=dictionary[dictionary['name']]
            cat_id=[]
            for id in cont_id:
                cat_id.append(get_category_id_from_id_cont(db,id))
            categories.append({'values':cont_id,'cat_id':cat_id})
    # update paper data
    cursor.execute('''UPDATE paper SET title=%s,library=%s,code_name=%s,year=%s,abstract=%s,summary=%s, source=%s
    where id=%s''', (title,library,code_name,year,abstract,summary,source,paper_id))
    # update authors
    update_authors_to_paper(db, paper_id, authors)
    # update categories
    update_categories_data_from_dict_array(db, categories, paper_id)
    # Commit changes in the database
    db.connection.commit()


def update_authors_to_paper(db, paper_id, authors):
    cursor = db.connection.cursor()
    # remove authors from paper
    cursor.execute("DELETE FROM paper_has_authors WHERE paper_id=%s",[paper_id])
    # add authors again
    add_authors_to_paper(db, paper_id, authors)
    # Commit changes in the database
    db.connection.commit()


def update_categories_data_from_dict_array(db, categories, paper_id):
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM paper_has_cont WHERE paper_id=%s",(paper_id))
    add_data_to_categories_from_dict_array(db, categories, paper_id)



#-------------------------Funciones para Data---------------------------
#-----Author-----
def get_data_from_authors_as_headers_and_column_data(db):
    cursor = db.connection.cursor()
    # headers is a dict array
    headers = []
    category_columns = []
    cursor.execute("SHOW COLUMNS FROM author")
    for row in cursor.fetchall():
        col_type = parse_type(row[1])
        name = (row[0]).replace("_"," ")
        headers.append({'name': name,'type': col_type})
        category_columns.append({'name': name,'type': col_type})
    rows = []
    # get all data/rows from category
    cursor.execute("SELECT * FROM author")
    for row in cursor.fetchall():
        # - save column data from category table
        dict_row = {}
        i = 0
        for column in category_columns:
            dict_row[column['name']] = row[i]
            i += 1
        rows.append(dict_row)
    return {'headers':headers,'rows':rows}

def modify_author(db, author_id, author_name, author_affiliation):
    cursor = db.connection.cursor()
    cursor.execute("UPDATE author SET name=%s, affiliation=%s WHERE id=%s",(author_name, author_affiliation, author_id))
    # Commit changes in the database
    db.connection.commit()

def add_author(db, author_name, author_affiliation):
    cursor = db.connection.cursor()
    cursor.execute("INSERT INTO author (name, affiliation) values (%s,%s)",(author_name,author_affiliation))
    # Commit changes in the database
    db.connection.commit()

#-----Categories-----



#-------------------------Funciones para Categories---------------------------
def get_columns_data_types():
    return ['varchar', 'number', 'text']

def get_all_properties_from_category_as_dict_array(db, cat_id):
    cursor = db.connection.cursor()
    dict_array = []
    # get all columns from the category table and create properties
    cursor.execute("show columns from categories")
    for row in cursor.fetchall():
        if row[0] == 'id' or row[0] == 'extra':
            continue
        # - add 'type' to the dictionary
        type = parse_type(row[1])
        # - set 'is_subcat' to false
        dict_array.append({'name':row[0],'type':type,'is_subcat':False,'properties':[]})
    cursor.execute("SELECT extra FROM categories WHERE id=%s",(cat_id))
    extra=cursor.fetchall()
    extra1=re.split(';',extra[0][0])
    for i in extra1:
        if i=='':
            continue
        dict_array.append({'name':i,'type':'varchar','is_subcat':False,'properties':[]})
    # get all subcategories from category
    subcats_id = get_all_subcategories_id_of_category_as_array(db, cat_id)
    for subcat_id in subcats_id:
        subcat_name = get_subcategory_name_from_id(db, subcat_id)
        # - for each subcategory, get their columns and add it to their properties
        properties_type = get_subcategory_properties_type_as_dict(db,subcat_id)
        properties = [name for name in properties_type]
        # - add 'type'='subcat' to the dictionary
        type = 'subcat'
        # - set 'is_subcat' to true
        is_subcat = 'True'
        cursor.execute("SELECT name FROM interaction WHERE id IN (SELECT int_id FROM int_cont WHERE cont_id=%s or cont_id=%s)",[subcat_id,subcat_id])
        for row in cursor.fetchall():
            interaction = row[0]
            dict_array.append({'name':subcat_name,'id':subcat_id,'properties':properties, 'properties_type':properties_type,
                           'type':type,'is_subcat':is_subcat,'interaction':interaction})
    return dict_array

def delete_category_column(db, cat_id,column_name):
    cursor = db.connection.cursor()
    cursor.execute("SELECT extra FROM categories WHERE id=%s",(cat_id))
    extra=cursor.fetchall()
    while re.search(r"\$[^$;]*;", extra):
        texto = re.sub(r"\$[^$;]*;", ";", extra, count=1)
    extra1=re.split(';',extra1[0][0])
    extranew=""
    for i in extra1:
        if i==column_name or i=="":
            continue
        else:
            extranew+=i+";"
    # delete column
    cursor.execute("UPDATE categories SET extra=%s WHERE id=%s",(extranew,cat_id))
    # Commit changes in the database
    db.connection.commit()

def get_all_subcategories_id_of_category_as_array(db, cat_id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT DISTINCT cont_id FROM cat_cont WHERE cat_id=%s", [cat_id])
    subcat_id_array = []
    for row in cursor.fetchall():
        subcat_id_array.append(row[0])
    return subcat_id_array

def get_subcategory_name_from_id(db,cont_id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT name FROM content WHERE id=%s",[cont_id])
    for row in cursor.fetchall():
        return row[0]

def get_subcategory_properties_type_as_dict(db, subcat_id):
    cursor = db.connection.cursor()
    cursor.execute("show columns from content")
    prop_dict = {}
    for row in cursor.fetchall():
        if row[0] == 'id':
            continue
        type = parse_type(row[1])
        prop_dict[row[0]] = type
    return prop_dict

def create_category(db,name, description):
    cursor = db.connection.cursor()
    cursor.execute('''INSERT INTO categories (name, description, extra)
                  VALUES (%s, %s, %s)''', (name, description, ""))
    db.connection.commit()

def add_column_to_category(db, cat_id, col_name, col_data):
    cursor = db.connection.cursor()
    # add column to table
    cursor.execute("UPDATE categories SET extra=%s WHERE id=%s",(col_name+"$"+col_data+";",cat_id))
    # Commit changes in the database
    db.connection.commit()

def delete_category_by_id(db, cat_id):
    cursor = db.connection.cursor()
    # delete subcategories attached to this category
    # - get subcategories attached
    subcategories_id_list = get_all_subcategories_id_of_category_as_array(db, cat_id)
    # - delete subcategories
    cursor.execute("DELETE FROM paper_has_cont WHERE cat_id=%s",(cat_id))
    cursor.execute("DELETE FROM cat_cont WHERE cat_id=%s",(cat_id))
    for subcat_id in subcategories_id_list:
        delete_subcategory_by_id(db, subcat_id, cat_id)
    cursor.execute("DELETE FROM int_cat WHERE cat_id1=%s OR cat_id2=%s",(cat_id,cat_id))
    cursor.execute("DELETE FROM categories WHERE id=%s",(cat_id))
    db.connection.commit()

def delete_subcategory_by_id(db, subcat_id,cat_id):
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM int_cont WHERE cont_id1=%s OR cont_id2=%s",(subcat_id,subcat_id))
    cursor.execute("DELETE FROM content WHERE id=%s",(subcat_id))
    db.connection.commit()

def get_data_from_category_as_headers_and_column_data(db, cat_id):
    cursor = db.connection.cursor()
    # headers is a dict array
    headers = []
    category_columns = []
    # --------------------------------------------------------------------------------
    # get category columns
    cat_name = create_category_name(cat_id)
    cursor.execute("SHOW COLUMNS FROM "+cat_name)
    for row in cursor.fetchall():
        #if row[0] == 'id':
        #    continue
        col_type = parse_type(row[1])
        name = (row[0]).replace("_"," ")
        headers.append({'name': name,'type': col_type})
        category_columns.append({'name': name,'type': col_type})
    # get subcategories (without value) from category with cat_id
    cursor.execute('''SELECT cat_subcat_interactions.interaction, subcategories.name, subcategories.id
    FROM cat_subcat_interactions INNER JOIN subcategories ON cat_subcat_interactions.subcat_id=subcategories.id
     WHERE cat_subcat_interactions.cat_id=%s''',[cat_id])
    for row in cursor.fetchall():
        name = (row[0]+" "+row[1]).replace("_"," ")
        subcat_id = row[2]
        headers.append({'name':name,'type':'subcat','id':subcat_id,'rel_with_cat':row[0]})
    # --------------------------------------------------------------------------------

    # rows is a dict array
    # --------------------------------------------------------------------------------
    cursor_2 = db.connection.cursor()
    rows = []
    # get all data/rows from category
    cursor.execute("SELECT * FROM "+cat_name)
    for row in cursor.fetchall():
        id = row[0]
        # - save column data from category table
        dict_row = {}
        i = 0
        for column in category_columns:
            dict_row[column['name']] = row[i]
            i += 1
        # - with the id search for cat_interaction_subcat tables
        cat_interaction_subcat_table_names = []
        cursor_2.execute("SELECT interaction, subcat_id FROM cat_subcat_interactions WHERE cat_id=%s",[cat_id])
        for row_2 in cursor_2.fetchall():
            cat_interaction_subcat_table_names.append(
                {'table_name':create_cat_has_subcat_name(cat_id,row_2[1],row_2[0]),
                 'subcat_id':row_2[1],
                 'subcat_name':(row_2[0]+get_subcategory_name_from_id(db,row_2[1])).replace("_","").replace(" ","")})
        # - in those tables search for the subcat_id that matches the current id (from previous step)
        # - with those subcat_id go to the subcategory table and get their names
        for dictionary in cat_interaction_subcat_table_names:
            subcat_table_name = create_subcategory_name(dictionary['subcat_id'])
            get_names = "SELECT "+subcat_table_name+".name FROM "+dictionary['table_name']+" INNER JOIN "\
                        +subcat_table_name+" ON "+dictionary['table_name']+"."+subcat_table_name+"_id="+\
                        subcat_table_name+".id WHERE "+cat_name+"_id=%s"
            cursor_2.execute(get_names, [id])
            subcat_names_as_str = ""
            for row_2 in cursor_2.fetchall():
                subcat_names_as_str += row_2[0] + ";"
            dict_row[dictionary['subcat_name']] = subcat_names_as_str
        # - append subcategory name with value
        rows.append(dict_row)

    return {'headers':headers,'rows':rows}
