__author__ = 'ivana'
import re
from flask import jsonify, request

#-------------------------General Functions---------------------------
"""Function that returns the data type of a variable"""
def parse_type(type_name):
    if 'int' in type_name:
        return 'number'
    if 'number' in type_name:
        return 'number'
    if 'varchar' in type_name:
        return 'varchar'
    if 'text' in type_name:
        return 'text'
    else:
        return 'varchar'

"""Function to separate a list separated by ;"""    
def set_as_list(string):
    lst = string.split(";")
    return [ r for r in lst if r != '']

"""Function that delivers the data type"""
def get_columns_data_types():
    return ['varchar', 'number', 'text']

"""function to separate the information separated by ; and $ used in the extra attribute of category"""
def show_columns_category(db,cat_id):
    cursor = db.connection.cursor()
    dict_array = []
    # get all columns from the category table and create properties
    cursor.execute("show columns from categories")
    for row in cursor.fetchall():
        if row[0] == 'id' or row[0] == 'extra':
            continue
        else:
            # - add 'type' to the dictionary
            type = parse_type(row[1])
            # - set 'is_subcat' to false
            dict_array.append({'name':row[0],'type':type,'is_subcat':False,'properties':[]})
    print(f"cat_id: {cat_id}")
    cursor.execute("SELECT extra FROM categories WHERE id=%s", [int(cat_id)])
    row=cursor.fetchall()
    split_data = row[0][0].split(";")
    split_data = split_data[:-1]
    for i in split_data:
        data = i.split("$")
        if data[0] != '':
            type = parse_type(data[1])
            dict_array.append({'name':data[0],'type':type,'is_subcat':False,'properties':[]})
    return dict_array


#-------------------------Functions for Index---------------------------
#---Functions to display form to add paper---
"""Function to obtain the properties of a paper"""
def get_paper_properties(db):
    cursor = db.connection.cursor()
    dict_array = []
    # get columns
    cursor.execute("show columns from paper")
    for row in cursor.fetchall():
        if row[0] == 'id':
            continue #no id is add as it is generat automatically
        if row[0] == 'library':
            dict_array.append({'name':'authors','type':'text'}) #add the author because it is not found directly as a paper column.
        dict_array.append({'name':str(row[0]).replace("_"," "), 'type':parse_type(row[1])})
    # get categories
    cursor.execute("select id, name from categories")
    for row in cursor.fetchall():
        # - get categories data
        data = get_data_from_category_by_cat_id(db, row[0])
        dict_array.append({'name':row[1],'type':'category','data':data,'id':row[0]})
    return dict_array

"""Function to obtain the contents corresponding to a category"""
def get_data_from_category_by_cat_id(db, cat_id):
    cursor = db.connection.cursor()
    #select the content that is related to the category
    cursor.execute("SELECT id, name FROM content WHERE id IN (SELECT cont_id FROM cat_cont WHERE cat_id="+str(cat_id)+")")
    dict_array = []
    for row in cursor.fetchall():
        dict_array.append({'name':row[1],'id':row[0]})
    return dict_array

#---Functions for adding paper---
"""Function to add paper attributes to the DB"""
def add_paper_using_dict_array(db, dict_array):
    cursor = db.connection.cursor()
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

"""Function to obtain the id from the content name"""
def get_content_id_from_name(db,name):
    cursor = db.connection.cursor()
    cursor.execute("SELECT id FROM content WHERE name = %s", [name])
    category_id = ""
    for row in cursor.fetchall():
        category_id = row[0]
        break
    return category_id

"""Function to obtain the category id from the id of a content"""
def get_category_id_from_id_cont(db,id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT cat_id FROM cat_cont WHERE cont_id="+id)
    category_id = ""
    for row in cursor.fetchall():
        category_id = row[0]
        break
    return category_id

"""Function to get the paper id from the paper title"""
def get_paper_id_where_title_exactly(db, title):
    cursor = db.connection.cursor()
    cursor.execute("select id from paper where title=%s",[title])
    for row in cursor.fetchall():
        return row[0]
    
"""Funtion to add authors to a paper"""
def add_authors_to_paper(db, paper_id, authors):
    cursor = db.connection.cursor()
    for author in authors:
        id = get_or_create_author_id_from_name(db,author)
        cursor.execute("insert into paper_has_authors (paper_id, author_id) values (%s, %s)", (paper_id,id))
    db.connection.commit()

"""function to create or add an author"""
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

"""Funtion to create a categorie""" 
def add_data_to_categories_from_dict_array(db, categories, paper_id):
    cursor = db.connection.cursor()
    for category in categories:
        i=0
        for value in category['values']:
            cursor.execute("INSERT INTO paper_has_cont (paper_id, cat_id, cont_id) VALUES (%s,%s,%s)",(paper_id,category['cat_id'][i],value))
            i+=1

#---Search functions by name---            
"""Function to obtain the properties of a paper""" 
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

"""Function to obtain the authors of a paper""" 
def get_authors_from_paper_id_as_str(db, paper_id):
    cursor = db.connection.cursor()
    authors_str = ""
    cursor.execute("select author_id from paper_has_authors where paper_id=%s",[paper_id])
    for row in cursor.fetchall():
        authors_str += get_author_name_from_id(db,row[0]) + ";"
    return authors_str

"""Function to obtain the name associated with an id of an author"""
def get_author_name_from_id(db,author_id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT name FROM author WHERE id=%s",[author_id])
    for row in cursor.fetchall():
        return row[0]

"""Function to extract the contents associated with a paper id"""
def get_value_from_category_where_paper_id(db,paper_id,cat_id):
    cursor = db.connection.cursor()
    value = []
    cursor.execute("SELECT name FROM content WHERE id IN (select cont_id from paper_has_cont where paper_id =%s and cat_id=%s)", [paper_id, cat_id])
    for row in cursor.fetchall():
        value.append(row[0])
    return value

"""Funtion to obtain values from paper id"""
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

#---Functions for modifying a paper---
"""Funtion to edit a paper"""
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

"""Function to change the author of a paper"""
def update_authors_to_paper(db, paper_id, authors):
    cursor = db.connection.cursor()
    # remove authors from paper
    cursor.execute("DELETE FROM paper_has_authors WHERE paper_id=%s",[paper_id])
    # add authors again
    add_authors_to_paper(db, paper_id, authors)
    # Commit changes in the database
    db.connection.commit()

"""Function to edit the categories of a paper"""
def update_categories_data_from_dict_array(db, categories, paper_id):
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM paper_has_cont WHERE paper_id=%s",(paper_id))
    add_data_to_categories_from_dict_array(db, categories, paper_id)
    
    
"""Funtion to delete paper"""
def delete_paper_by_id(db, paper_id):
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM papers WHERE id=%s", (paper_id,))
    cursor.execute("DELETE FROM paper_has_authors WHERE paper_id=%s", (paper_id,))
    cursor.execute("DELETE FROM paper_has_cont WHERE paper_id=%s", (paper_id,))
    db.connection.commit()


#-------------------------Functions for Categories---------------------------
#---functions for displaying the page od Categories---
"""Funtion to"""
def get_all_categories_as_dict_array(db):
    cursor = db.connection.cursor()
    cursor.execute("SELECT id, name FROM categories")
    category_dict_array = []
    for row in cursor.fetchall():
        category_dict_array.append({'id':row[0],'name':row[1]})
    return category_dict_array

#---Functions to display the information of a Category--- ----------------------------ARREGLAR CUANDO PONGA EL TIPO DE DATO
"""Funtion to"""
def get_all_properties_from_category_as_dict_array(db, cat_id):
    cursor = db.connection.cursor()
    # get all columns from the category table and create properties
    dict_array = show_columns_category(db,cat_id)
    # get all subcategories from category
    subcats_id = get_all_content_id_of_category_as_array(db, cat_id)
    for subcat_id in subcats_id:
        subcat_name = get_content_name_from_id(db, subcat_id)
        # - for each subcategory, get their columns and add it to their properties
        properties_type = get_content_properties_type_as_dict(db,subcat_id)
        properties = [name for name in properties_type]
        # - add 'type'='subcat' to the dictionary
        type = 'subcat'
        # - set 'is_subcat' to true
        is_subcat = 'True'
        cursor.execute("SELECT name FROM interaction WHERE id IN (SELECT int_id FROM int_cat WHERE cat_id=%s)",[subcat_id])
        for row in cursor.fetchall():
            interaction = row[0]
            dict_array.append({'name':subcat_name,'id':subcat_id,'properties':properties, 'properties_type':properties_type,
                           'type':type,'is_subcat':is_subcat,'interaction':interaction})
    return dict_array

"""Function to get the name of a content through its id"""
def get_content_name_from_id(db,cont_id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT name FROM content WHERE id=%s",[cont_id])
    for row in cursor.fetchall():
        return row[0]

"""Funtion to obtain the type of content properties such as dict"""
def get_content_properties_type_as_dict(db, subcat_id):
    cursor = db.connection.cursor()
    cursor.execute("show columns from content")
    prop_dict = {}
    for row in cursor.fetchall():
        if row[0] == 'id':
            continue
        type = parse_type(row[1])
        prop_dict[row[0]] = type
    return prop_dict
    
"""Funtion to get the contents of a category"""
def get_all_content_id_of_category_as_array(db, cat_id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT DISTINCT cont_id FROM cat_cont WHERE cat_id=%s", [cat_id])
    subcat_id_array = []
    for row in cursor.fetchall():
        subcat_id_array.append(row[0])
    return subcat_id_array
 
#---Functions to manage the column of a category---
"""Funtion to add column to category""" 
def add_column_to_category(db, cat_id, col_name, col_data):
    cursor = db.connection.cursor()
    # add column to table
    cursor.execute("SELECT extra FROM categories WHERE id=%s",(cat_id))
    extra=str(cursor.fetchall()[0][0])
    extra+=col_name+"$"+col_data+";"
    cursor.execute("UPDATE categories SET extra=%s WHERE id=%s",(extra,cat_id))
    # Commit changes in the database
    db.connection.commit()

"""Funtion to delete column to category""" 
def delete_category_column(db, cat_id,column_name):
    cursor = db.connection.cursor()
    cursor.execute("SELECT extra FROM categories WHERE id=%s",(cat_id))
    tupla=cursor.fetchall()
    cadena = tupla[0][0]
    columnas = cadena.split(';')
    columnas = [columna.split('$') for columna in columnas]
    extranew=""
    m=0
    for i in columnas:
        if i[0]==column_name :
            n=m
        elif i[0]=='':
            pass
        else:
            m+=1
            extranew+=str(i[0])+"$"+str(i[1])+";"
    # delete column
    cursor.execute("UPDATE categories SET extra=%s WHERE id=%s",(extranew,cat_id)) 
    cursor.execute("SELECT cont_id FROM cat_cont WHERE cat_id=%s",(cat_id))   #----------------------------------------PROBAR CUANDO AGREGUE CONT
    for cont_id in cursor.fetchall():
        cursor.execute("SELECT extra FROM content WHERE id=%s",(cont_id))
        extra=cursor.fetchall()
        extra=re.split(';', extra[0][0])
        extranew=""
        x=0
        for i in extra:
            if x==n or "":
                pass
            else:
                extranew+=i+";"
            x+=1
        cursor.execute("UPDATE content SET extra=%s WHERE id=%s",(extranew,cont_id))
    # Commit changes in the database
    db.connection.commit()


#---Functions to manage a category---
"""Funtion to add category"""
def create_category(db,name, description):
    cursor = db.connection.cursor()
    cursor.execute('''INSERT INTO categories (name, description, extra)
                  VALUES (%s, %s, %s)''', (name, description, ""))
    db.connection.commit()

"""Funtion to delete category"""
def delete_category_by_id(db, cat_id):
    cursor = db.connection.cursor()
    # delete subcategories attached to this category
    # - get subcategories attached
    subcategories_id_list = get_all_subcategories_id_of_category_as_array(db, cat_id)
    # - delete subcategories
    cursor.execute("DELETE FROM paper_has_cont WHERE cat_id=%s",(cat_id))
    cursor.execute("DELETE FROM cat_cont WHERE cat_id=%s",(cat_id))
    for subcat_id in subcategories_id_list:
        delete_subcategory_by_id(db, subcat_id)
    cursor.execute("DELETE FROM int_cat WHERE cat_id1=%s OR cat_id2=%s",(cat_id,cat_id))
    cursor.execute("DELETE FROM categories WHERE id=%s",(cat_id))
    db.connection.commit()

"""function to obtain contents associated to a category"""
def get_all_subcategories_id_of_category_as_array(db, cat_id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT DISTINCT cont_id FROM cat_cont WHERE cat_id=%s", [cat_id])
    subcat_id_array = []
    for row in cursor.fetchall():
        subcat_id_array.append(row[0])
    return subcat_id_array

"""Funtion to delete content"""
def delete_subcategory_by_id(db, subcat_id):
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM content WHERE id=%s",(subcat_id))
    cursor.execute("DELETE FROM cat_cont WHERE cont_id=%s",(subcat_id))
    db.connection.commit()

#-------------------------Functions for Data---------------------------
#---functions for displaying author data and their respective functionalities---

"""Funtion to obtain the authors' information"""
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


"""Function to modify an author"""
def modify_author(db, author_id, author_name, author_affiliation):
    cursor = db.connection.cursor()
    cursor.execute("UPDATE author SET name=%s, affiliation=%s WHERE id=%s",(author_name, author_affiliation, author_id))
    # Commit changes in the database
    db.connection.commit()

"""Funtion to add an author"""
def add_author(db, author_name, author_affiliation):
    cursor = db.connection.cursor()
    cursor.execute("INSERT INTO author (name, affiliation) values (%s,%s)",(author_name,author_affiliation))
    # Commit changes in the database
    db.connection.commit()

"""Funtion to delete an author"""
def delete_author(db, author_id):
    cursor = db.connection.cursor()
    cursor.execute("DELETE FROM paper_has_authors WHERE author_id=%s",author_id)
    cursor.execute("DELETE FROM author WHERE id=%s",author_id)
    # Commit changes in the database
    db.connection.commit()

#---functions to add, edit or delete content---
"""Function to add a content to a category"""
def add_data_row_to_category(db,cat_id,dict_array):
    cursor = db.connection.cursor()
    prop_str = []
    values_str = "("
    values = ()
    n=0
    for element in dict_array:   ####ARREGLAR SADASDSADSADASDASDASDSADSAD
        if not element['is_subcat']:
            if element['id_name']=='name':
                prop_str.append(element[element['id_name']])
                values_str = values_str + "%s,"
                values += (element[element['id_name']],)
            elif element['id_name']=='description':
                prop_str.append(element[element['id_name']])
                values_str = values_str + "%s,"
                values += (element[element['id_name']],)
                prop_str.append("")
            else:
                if n==0:
                    prop_str[2]+=element[element['id_name']]
                    values_str = values_str + "%s,"
                    values += (element[element['id_name']],)
                    n+=1
                else:
                    prop_str[2]+=";"+element[element['id_name']]
                    values += (element[element['id_name']],)

    # finish strings
    values_str = values_str[0:len(values_str)-1]+")"
    # add new row to category table
    cursor.execute("INSERT INTO content (name, description, extra) VALUES (%s,%s,%s)", (prop_str[0],prop_str[1],prop_str[2]))
    last_id = cursor.lastrowid
    cursor.execute("INSERT INTO cat_cont (cat_id, cont_id) VALUES (%s, %s)", (cat_id, last_id))
    #cursor.execute("INSERT INTO "+cat_table_name+" "+prop_str+" values "+values_str,values)
    ## get new row id
    #new_cat_element_id = get_row_id_from_category_by_name(db, cat_id, name_of_new_element)
    #for element in dict_array:
    #    if element['is_subcat']:
    #        # in this case we have that the value is from a subcategory of this category
    #        subcat_id = element['id']
    #        subcat_table_name = create_subcategory_name(subcat_id)
    #        rel_table_name = create_cat_has_subcat_name(cat_id,subcat_id,element['rel_with_cat'])
    #        for value in element[element['id_name']]:
    #            # note that the subcat value already exists in that table so the relation it's the only thing to be added
    #            cursor.execute("INSERT INTO "+rel_table_name+" ("+cat_table_name+"_id,"+subcat_table_name+"_id) values (%s,%s)",
    #                           (new_cat_element_id,value))
    # Commit changes in the database
    db.connection.commit()

#---functions for displaying category data and their respective functionalities---
"""Function to remove duplicate subcategories"""
def remove_subcategories_duplicated(dict_array_subcategories):
    dict_array = []##########    EDITAR--------------------------------------------------
    subcat_ids_added = []
    for element in dict_array_subcategories:
        if element['is_subcat']:
            if element['id'] not in subcat_ids_added:
                subcat_ids_added.append(element['id'])
                dict_array.append(element)
        else:
            dict_array.append(element)
    return dict_array
 
"""Function to obtain category information"""
def get_data_from_category_as_headers_and_column_data(db, cat_id):
    cursor = db.connection.cursor()
    headers=show_columns_category(db,cat_id)
    cursor.execute("SELECT cont_id FROM cat_cont WHERE cat_id=%s",cat_id)
    result = cursor.fetchall()
    rows = []
    for cont_id in result:
        cursor.execute("SELECT name, description, extra FROM content WHERE id=%s", (cont_id[0],))
        row = cursor.fetchall()
        row_dict = {}
        for row_data in row:
            row_dict['name'] = row_data[0]
            row_dict['description'] = row_data[1]
            extras = row_data[2].split(';')  # Separar la columna 'extra' por el carácter ';'
            for extra,i in enumerate(extras, start=2):
                if extra<len(headers):
                    name=headers[extra]['name']
                    row_dict[name] = i
            rows.append(row_dict.copy())
    return {'headers':headers,'rows':rows}

#---functions for edit and delete a category---
"""Function to remove a content from a category"""
def delete_row_from_category(db, cat_id, row_id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT cont_id FROM cat_cont WHERE cat_id=%s", (cat_id))
    cont_id= cursor.fetchall()[int(row_id)][0]

    cursor.execute("DELETE FROM paper_has_cont WHERE cont_id=%s",(cont_id,))###Update or delete?
    cursor.execute("DELETE FROM cat_cont WHERE cont_id=%s",(cont_id,))

    cursor.execute("DELETE FROM content WHERE id=%s",(cont_id,))
    db.connection.commit()

"""Function to edit a content"""
def edit_data_row_to_category(db, cat_id, row_id, dict_array):
    cursor = db.connection.cursor()
    cursor = db.connection.cursor()
    cursor.execute("SELECT cont_id FROM cat_cont WHERE cat_id=%s", (cat_id))
    cont_id= cursor.fetchall()[int(row_id)][0]
    prop_str = []
    values_str = "("
    values = ()
    n=0
    for element in dict_array:   
        if not element['is_subcat']:
            if element['id_name']=='name':
                prop_str.append(element[element['id_name']])
                values_str = values_str + "%s,"
                values += (element[element['id_name']],)
            elif element['id_name']=='description':
                prop_str.append(element[element['id_name']])
                values_str = values_str + "%s,"
                values += (element[element['id_name']],)
                prop_str.append("")
            else:
                if n==0:
                    prop_str[2]+=element[element['id_name']]
                    values_str = values_str + "%s,"
                    values += (element[element['id_name']],)
                    n+=1
                else:
                    prop_str[2]+=";"+element[element['id_name']]
                    values += (element[element['id_name']],)
    # finish strings
    values_str = values_str[0:len(values_str)-1]+")"
    # add new row to category table
    cursor.execute("UPDATE content SET name=%s,description=%s,extra=%s WHERE id=%s", (prop_str[0],prop_str[1],prop_str[2],cont_id))
    db.connection.commit()

"""Function to create a interaction"""
def create_subcategory(db,name,cat_id,interaction):
    cursor = db.connection.cursor()
    cursor.execute("INSERT INTO interaction (name) VALUES (%s)",[name])
    nuevo_id = cursor.lastrowid
    cursor.execute("INSERT INTO int_cat (cat_id,int_id,name) VALUES (%s,%s,%s)",[cat_id,nuevo_id,interaction])
    db.connection.commit()

#-------------------------Functions for Search---------------------------

#---functions for displaying search---
"""Function to get the name of the category from the id"""
def get_category_name_from_id(db, cat_id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT name FROM categories WHERE id=%s",[cat_id])
    for row in cursor.fetchall():
        return row[0]


#-------------------------Functions for Search--------------------------- 

# Function to fetch autocomplete suggestions from the database
def get_suggestions(db):
    cursor = db.connection.cursor()
    user_input = request.args.get('input')
    if (user_input): 
        
        sql = "SELECT title FROM paper WHERE title LIKE %s LIMIT 10"
        cursor.execute(sql, (user_input + '%',))

        suggestions = cursor.fetchall()
        paper_titles = [paper[0] for paper in suggestions]
        return jsonify({'suggestions': paper_titles})
         
    return jsonify({'suggestions': []})






