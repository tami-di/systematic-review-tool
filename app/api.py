__author__ = 'ivana'

#-------------------------General Functions---------------------------
"""Function that returns the data type of a variable"""
def parse_type(type_name):
    if 'int' in type_name:
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

#-------------------------Functions for Index---------------------------

#---Functions to display form to add paper---
"""Funtion to"""
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

"""Funtion to"""
def get_data_from_category_by_cat_id(db, cat_id):
    cursor = db.connection.cursor()
    #select the content that is related to the category
    cursor.execute("SELECT id, name FROM content WHERE id IN (SELECT cont_id FROM cat_cont WHERE cat_id="+str(cat_id)+")")
    dict_array = []
    for row in cursor.fetchall():
        dict_array.append({'name':row[1],'id':row[0]})
    return dict_array

#---functions for adding paper---
"""Funtion to"""
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


"""Funtion to"""
def get_content_id_from_name(db,name):
    cursor = db.connection.cursor()
    cursor.execute("SELECT id FROM content WHERE name = %s", [name])
    category_id = ""
    for row in cursor.fetchall():
        category_id = row[0]
        break
    return category_id

"""Funtion to"""
def get_category_id_from_id_cont(db,id):
    cursor = db.connection.cursor()
    cursor.execute("SELECT cat_id FROM cat_cont WHERE cont_id="+id)
    category_id = ""
    for row in cursor.fetchall():
        category_id = row[0]
        break
    return category_id

"""Funtion to"""
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

"""Funtion to"""
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

"""Funtion to""" 
def add_data_to_categories_from_dict_array(db, categories, paper_id):
    cursor = db.connection.cursor()
    for category in categories:
        i=0
        for value in category['values']:
            cursor.execute("INSERT INTO paper_has_cont (paper_id, cat_id, cont_id) VALUES (%s,%s,%s)",(paper_id,category['cat_id'][i],value))
            i+=1

#---Search functions by name---            
"""Funtion to""" 
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

"""Funtion to""" 
def get_authors_from_paper_id_as_str(db, paper_id):
    cursor = db.connection.cursor()
    authors_str = ""
    cursor.execute("select author_id from paper_has_authors where paper_id=%s",[paper_id])
    for row in cursor.fetchall():
        authors_str += get_author_name_from_id(db,row[0]) + ";"
    return authors_str

"""Funtion to"""
def get_author_name_from_id(db,author_id):
    cursor = db.connection.cursor()
    cursor.execute("select name from author where id=%s",[author_id])
    for row in cursor.fetchall():
        return row[0]

"""Funtion to"""
def get_value_from_category_where_paper_id(db,paper_id,cat_id):
    cursor = db.connection.cursor()
    value = []
    cursor.execute("SELECT name FROM content WHERE id IN (select cont_id from paper_has_cont where paper_id =%s and cat_id=%s)", [paper_id, cat_id])
    for row in cursor.fetchall():
        value.append(row[0])
    return value

"""Funtion to"""
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
"""Funtion to"""
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