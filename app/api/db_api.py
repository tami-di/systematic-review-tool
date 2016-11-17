__author__ = 'ivana'
from sets import Set

def create_category_name(category_id):
    return "cat"+str(category_id)


def create_paper_has_category_name(category_id):
    return "paper_has_"+create_category_name(category_id)


def get_category_id_from_name(db,name):
    cursor = db.cursor()
    cursor.execute("SELECT id FROM categories WHERE name = %s", [name])
    category_id = ""
    for row in cursor.fetchall():
        category_id = row[0]
        break
    return category_id


def get_subcategory_id_from_name(db,name):
    cursor = db.cursor()
    cursor.execute('''SELECT id FROM subcategories WHERE name = %s''', [name])
    subcategory_id = ""
    for row in cursor.fetchall():
        subcategory_id = row[0]
        break
    return subcategory_id


def create_subcategory_name(subcat_id):
    return "subcat"+str(subcat_id)


def create_cat_has_subcat_name(cat_id,subcat_id,interaction):
    return "cat"+str(cat_id)+"_"+str(interaction)+"_subcat"+str(subcat_id)


def create_category(db,name, description):
    cursor = db.cursor()
    cursor.execute('''INSERT INTO categories (name, description)
                  VALUES (%s, %s)''', (name, description))
    category_id = get_category_id_from_name(db,name)
    # make the in-database name of table and category
    cat_name = create_category_name(category_id)
    paper_has_cat_name = create_paper_has_category_name(category_id)
    # command to create table, columns haven't been decided yet
    create_category_table = '''CREATE TABLE '''+cat_name+'''(id MEDIUMINT NOT NULL AUTO_INCREMENT primary key,
    name VARCHAR(100), description text)'''
    cursor.execute(create_category_table)
    # command to create relacional table between the category table and the paper
    create_relation_table = '''CREATE TABLE '''+paper_has_cat_name+'''(paper_id INT,'''+cat_name+'''_id MEDIUMINT,
    FOREIGN KEY (paper_id) REFERENCES paper(id), FOREIGN KEY ('''+cat_name+'''_id) REFERENCES '''+cat_name+'''(id))'''
    cursor.execute(create_relation_table)
    # Commit changes in the database
    db.commit()


def create_subcategory(db,name,cat_id,interaction):
    cursor = db.cursor()
    # insert new subcategory in table
    cursor.execute('''INSERT INTO subcategories (name) VALUES (%s)''',[name])
    # get subcategory id
    subcategory_id = get_subcategory_id_from_name(db,name)
    # add interaction of category and subcategory to table
    cursor.execute('''INSERT INTO cat_subcat_interactions (cat_id,interaction,subcat_id) VALUES (%s,%s,%s)''',
                   (cat_id,interaction,subcategory_id))
    # create subcategory table
    subcategory_name = create_subcategory_name(subcategory_id)
    create_subcategory_table = '''CREATE TABLE '''+subcategory_name+'''
    (id MEDIUMINT NOT NULL AUTO_INCREMENT primary key, name VARCHAR(100), description text)'''
    cursor.execute(create_subcategory_table)
    # create cat_interaction_subcat table
    interaction_table_name = create_cat_has_subcat_name(cat_id,subcategory_id,interaction)
    category_name = create_category_name(cat_id)
    create_relation_table = '''CREATE TABLE '''+interaction_table_name+'''('''+category_name+'''_id MEDIUMINT,'''+\
                            subcategory_name+'''_id MEDIUMINT,
    FOREIGN KEY ('''+category_name+'''_id) REFERENCES '''+category_name+'''(id), FOREIGN KEY ('''+\
                            subcategory_name+'''_id) REFERENCES '''+subcategory_name+'''(id))'''
    cursor.execute(create_relation_table)
    # Commit changes in the database
    db.commit()


def add_column_to_subcategory(db, subcat_id, col_name, col_data):
    cursor = db.cursor()
    # add column to table
    cursor.execute("ALTER TABLE "+create_subcategory_name(subcat_id)+" ADD "+col_name+" "+unparse_type(col_data))
    # Commit changes in the database
    db.commit()


def add_column_to_category(db, cat_id, col_name, col_data):
    cursor = db.cursor()
    # add column to table
    cursor.execute("ALTER TABLE "+create_category_name(cat_id)+" ADD "+col_name+" "+unparse_type(col_data))
    # Commit changes in the database
    db.commit()


def get_all_categories_as_dict_array(db):
    cursor = db.cursor()
    cursor.execute("SELECT id, name FROM categories")
    category_dict_array = []
    for row in cursor.fetchall():
        category_dict_array.append({'id':row[0],'name':row[1]})
    return category_dict_array


def delete_category_column(db, cat_id,column_name):
    cursor = db.cursor()
    # delete column
    cursor.execute("ALTER TABLE "+create_category_name(cat_id)+" DROP COLUMN "+column_name)
    # Commit changes in the database
    db.commit()


def delete_category_by_id(db, cat_id):
    cursor = db.cursor()
    cat_name = create_category_name(cat_id)
    paper_has_cat_name = create_paper_has_category_name(cat_id)
    # delete subcategories attached to this category
    # - get subcategories attached
    subcategories_id_list = get_all_subcategories_id_of_category_as_array(db, cat_id)
    # - delete subcategories
    for subcat_id in subcategories_id_list:
        delete_subcategory_by_id(db, subcat_id, cat_id=cat_id)
    cursor.execute("DROP TABLE "+paper_has_cat_name)
    # delete category table
    cursor.execute("DROP TABLE "+cat_name)
    # delete reference to table in categories
    cursor.execute("DELETE FROM categories WHERE id=%s", [cat_id])
    # Commit changes in the database
    db.commit()


def delete_subcategory_by_id(db, subcat_id,cat_id=""):
    cursor = db.cursor()
    # get category id associated to this subcategory, it should be one exactly
    if cat_id == "":
        cursor.excute("SELECT DISTINCT cat_id FROM cat_subcat_interactions WHERE subcat_id=%s", [subcat_id])
        for row in cursor.fetchall():
            cat_id = row[0]
    # delete table cat_has_subcat
    tables_to_delete = []
    cursor.execute("SELECT interaction FROM cat_subcat_interactions WHERE cat_id=%s and subcat_id=%s",
                   (cat_id, subcat_id))
    for row in cursor.fetchall():
        interaction_name = row[0]
        tables_to_delete.append(create_cat_has_subcat_name(cat_id, subcat_id, interaction_name))
    for cat_has_subcat_name in tables_to_delete:
        cursor.execute("DROP TABLE "+cat_has_subcat_name)
    # delete table subcat
    subcategory_name = create_subcategory_name(subcat_id)
    cursor.execute("DROP TABLE "+subcategory_name)
    # delete reference to relation between category and subcategory in cat_subcat_interactions
    cursor.execute("DELETE FROM cat_subcat_interactions where subcat_id=%s and cat_id=%s", (subcat_id,cat_id))
    # delete reference to subcat in subcategories table
    cursor.execute("DELETE FROM subcategories where id=%s", [subcat_id])
    # Commit changes in the database
    db.commit()


def get_all_subcategories_id_of_category_as_array(db, cat_id):
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT subcat_id FROM cat_subcat_interactions where cat_id=%s", [cat_id])
    subcat_id_array = []
    for row in cursor.fetchall():
        subcat_id_array.append(row[0])
    return subcat_id_array


def get_all_properties_from_category_as_dict_array(db, cat_id):
    cursor = db.cursor()
    dict_array = []
    # get all columns from the category table and create properties
    cursor.execute("show columns from "+create_category_name(cat_id))
    for row in cursor.fetchall():
        if row[0] == 'id':
            continue
        # - add 'type' to the dictionary
        type = parse_type(row[1])
        # - set 'is_subcat' to false
        dict_array.append({'name':row[0],'type':type,'is_subcat':False,'properties':[]})

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
        cursor.execute("SELECT interaction FROM cat_subcat_interactions WHERE subcat_id=%s",[subcat_id])
        for row in cursor.fetchall():
            interaction = row[0]
            dict_array.append({'name':subcat_name,'id':subcat_id,'properties':properties, 'properties_type':properties_type,
                           'type':type,'is_subcat':is_subcat,'interaction':interaction})
    return dict_array


def get_subcategory_properties_type_as_dict(db, subcat_id):
    cursor = db.cursor()
    cursor.execute("show columns from "+create_subcategory_name(subcat_id))
    prop_dict = {}
    for row in cursor.fetchall():
        if row[0] == 'id':
            continue
        type = parse_type(row[1])
        prop_dict[row[0]] = type
    return prop_dict


def get_subcategory_name_from_id(db,subcat_id):
    cursor = db.cursor()
    cursor.execute("SELECT name FROM subcategories WHERE id=%s",[subcat_id])
    for row in cursor.fetchall():
        return row[0]


def get_paper_properties(db):
    cursor = db.cursor()
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


def get_paper_properties_and_values_on_table_format(db, paper_id):
    dict_array = get_paper_properties_and_values(db, paper_id)
    dict_result = {}
    for dictionary in dict_array:
        if dictionary['type'] == 'category':
            str_value = ""
            for value in dictionary['value']:
                str_value = str_value + str(value) +";"
            dict_result[dictionary['name']] = str_value
        else:
            dict_result[dictionary['name']] = dictionary['value']
    return dict_result


def get_authors_from_paper_id_as_str(db, paper_id):
    cursor = db.cursor()
    authors_str = ""
    cursor.execute("select author_id from paper_has_authors where paper_id=%s",[paper_id])
    for row in cursor.fetchall():
        authors_str = authors_str + get_author_name_from_id(db,row[0]) + ";"
    return authors_str


def get_author_name_from_id(db,author_id):
    cursor = db.cursor()
    cursor.execute("select name from author where id=%s",[author_id])
    for row in cursor.fetchall():
        return row[0]


def get_author_id_from_name(db,author_name):
    cursor = db.cursor()
    cursor.execute("select id from author where name=%s",[author_name])
    for row in cursor.fetchall():
        return row[0]


def get_value_from_category_where_paper_id(db,paper_id,cat_id):
    cursor = db.cursor()
    value = []
    cat_name = create_category_name(cat_id)
    paper_has_cat_name = create_paper_has_category_name(cat_id)
    cursor.execute("select name from "+cat_name+" where id in (select "+cat_name+"_id from "+paper_has_cat_name+" "
            " where paper_id = "+ str(paper_id) +")")
    for row in cursor.fetchall():
        value.append(row[0])
    return value


def edit_paper_using_dict_array(db, paper_id,dict_array):
    cursor = db.cursor()
    title = ""
    library = ""
    code_name = ""
    year = ""
    abstract = ""
    summary = ""
    categories = []
    authors = ""
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
        elif dictionary['name'] == 'authors':
            authors = set_as_list(dictionary['authors'])
        else:
            cat_id = get_category_id_from_name(db,dictionary['name'])
            cat_name = create_category_name(cat_id)
            table_name = create_paper_has_category_name(cat_id)
            categories.append({'table_name': table_name,'values': dictionary[dictionary['name']],'cat_name': cat_name})
    # update paper data
    cursor.execute('''UPDATE paper SET title=%s,library=%s,code_name=%s,year=%s,abstract=%s,summary=%s
    where id=%s''', (title,library,code_name,year,abstract,summary,paper_id))
    # update authors
    update_authors_to_paper(db, paper_id, authors)
    # update categories
    update_categories_data_from_dict_array(db, categories, paper_id)
    # Commit changes in the database
    db.commit()


def update_categories_data_from_dict_array(db, categories, paper_id):
    cursor = db.cursor()
    for category in categories:
        cursor.execute("DELETE FROM "+category['table_name']+" WHERE paper_id=%s",[paper_id])
    add_data_to_categories_from_dict_array(db, categories, paper_id)


def update_authors_to_paper(db, paper_id, authors):
    cursor = db.cursor()
    # remove authors from paper
    cursor.execute("DELETE FROM paper_has_authors WHERE paper_id=%s",[paper_id])
    # add authors again
    add_authors_to_paper(db, paper_id, authors)
    # Commit changes in the database
    db.commit()


def add_paper_using_dict_array(db, dict_array):
    cursor = db.cursor()
    title = ""
    library = ""
    code_name = ""
    year = ""
    abstract = ""
    summary = ""
    categories = []
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
        elif dictionary['name'] == 'authors':
            authors = set_as_list(dictionary['authors'])
        else:
            cat_id = get_category_id_from_name(db,dictionary['name'])
            cat_name = create_category_name(cat_id)
            table_name = create_paper_has_category_name(cat_id)
            categories.append({'table_name':table_name,'values':dictionary[dictionary['name']],'cat_name':cat_name})
    # add paper data
    cursor.execute('''insert into paper (title, library, code_name, year, abstract, summary) values
    (%s,%s,%s,%s,%s,%s)''', (title, library, code_name, year, abstract, summary))
    # get paper_id
    paper_id = get_paper_id_where_title_exactly(db, title)
    # add authors data
    add_authors_to_paper(db, paper_id, authors)
    # add category data
    add_data_to_categories_from_dict_array(db, categories, paper_id)
    # Commit changes in the database
    db.commit()


def get_row_id_from_category_by_name(db, cat_id, name):
    cursor = db.cursor()
    cat_table_name = create_category_name(cat_id)
    cursor.execute("SELECT id FROM "+cat_table_name+" WHERE name=%s",[name])
    for row in cursor.fetchall():
        return row[0]


def edit_data_row_to_category(db, cat_id, row_id, dict_array):
    cursor = db.cursor()
    cat_table_name = create_category_name(cat_id)
    set_str = ""
    values = ()
    for element in dict_array:
        if not element['is_subcat']:
            set_str = set_str + element['id_name'] + "=%s,"
            values += (element[element['id_name']],)
        else:
            # delete previous relations in cat_interaction_subcat
            subcat_id = element['id']
            subcat_table_name = create_subcategory_name(subcat_id)
            relation = element['rel_with_cat']
            rel_table = create_cat_has_subcat_name(cat_id,subcat_id,relation)
            cursor.execute("DELETE FROM "+rel_table+" WHERE "+cat_table_name+"_id=%s",[row_id])
            # append new relations
            for value in element[element['id_name']]:
                # note that the subcat value already exists in that table so the relation it's the only thing to be added
                cursor.execute("INSERT INTO "+rel_table+" ("+cat_table_name+"_id,"+subcat_table_name+"_id) values (%s,%s)",
                               (row_id,value))
    # finish string
    set_str = set_str[0:len(set_str)-1]
    # finish tuple
    values += (row_id,)
    # update columns of table
    cursor.execute("UPDATE "+cat_table_name+" SET "+set_str+" WHERE id=%s",values)
    # Commit changes in the database
    db.commit()


def add_data_row_to_category(db,cat_id,dict_array):
    cursor = db.cursor()
    cat_table_name = create_category_name(cat_id)
    new_cat_element_id = ""
    prop_str = "("
    values_str = "("
    values = ()
    name_of_new_element = ""
    for element in dict_array:
        if not element['is_subcat']:
            prop_str = prop_str + element['id_name'] + ","
            values_str = values_str + "%s,"
            values += (element[element['id_name']],)
            if element['id_name'] == 'name':
                name_of_new_element = element['name']
    # finish strings
    prop_str = prop_str[0:len(prop_str)-1]+")"
    values_str = values_str[0:len(values_str)-1]+")"
    # add new row to category table
    cursor.execute("INSERT INTO "+cat_table_name+" "+prop_str+" values "+values_str,values)
    # get new row id
    new_cat_element_id = get_row_id_from_category_by_name(db, cat_id, name_of_new_element)
    for element in dict_array:
        if element['is_subcat']:
            # in this case we have that the value is from a subcategory of this category
            subcat_id = element['id']
            subcat_table_name = create_subcategory_name(subcat_id)
            rel_table_name = create_cat_has_subcat_name(cat_id,subcat_id,element['rel_with_cat'])
            for value in element[element['id_name']]:
                # note that the subcat value already exists in that table so the relation it's the only thing to be added
                cursor.execute("INSERT INTO "+rel_table_name+" ("+cat_table_name+"_id,"+subcat_table_name+"_id) values (%s,%s)",
                               (new_cat_element_id,value))
    # Commit changes in the database
    db.commit()


def add_data_row_to_subcategory(db,subcat_id,dict_array):
    cursor = db.cursor()
    subcat_table_name = create_subcategory_name(subcat_id)
    prop_str = "("
    values_str = "("
    values = ()
    for element in dict_array:
        prop_str = prop_str + element['id_name'] + ","
        values_str += "%s,"
        values += (element[element['id_name']],)
    # finish strings
    prop_str = prop_str[0:len(prop_str)-1]+")"
    values_str = values_str[0:len(values_str)-1]+")"
    # add new row to category table
    cursor.execute("INSERT INTO "+subcat_table_name+" "+prop_str+" values "+values_str,values)
    # Commit changes in the database
    db.commit()


def edit_data_row_to_subcategory(db,subcat_id,row_id,dict_array):
    cursor = db.cursor()
    subcat_table_name = create_subcategory_name(subcat_id)
    set_str = ""
    values = ()
    for element in dict_array:
        set_str = set_str + element['id_name'] + "=%s,"
        values += (element[element['id_name']],)
    # finish string
    set_str = set_str[0:len(set_str)-1]
    # finish tuple
    values += (row_id,)
    # update columns of table
    cursor.execute("UPDATE "+subcat_table_name+" SET "+set_str+" WHERE id=%s",values)
    # Commit changes in the database
    db.commit()


def add_authors_to_paper(db, paper_id, authors):
    cursor = db.cursor()
    for author in authors:
        id = get_author_id_from_name(db,author)
        cursor.execute("insert into paper_has_authors (paper_id, author_id) values (%s, %s)", (paper_id,id))
    # Commit changes in the database
    db.commit()


def add_data_to_categories_from_dict_array(db, categories, paper_id):
    cursor = db.cursor()
    for category in categories:
        for value in category['values']:
            cursor.execute("insert into "+category['table_name']+" (paper_id,"+category['cat_name']+
                           "_id) values (%s,%s)",(paper_id,value))


def get_data_from_subategory_as_headers_and_column_data(db, subcat_id):
    cursor = db.cursor()
    subcat_name = create_subcategory_name(subcat_id)
    # headers is a dict array
    headers = []
    category_columns = []
    cursor.execute("SHOW COLUMNS FROM "+subcat_name)
    for row in cursor.fetchall():
        #if row[0] == 'id':
        #    continue
        col_type = parse_type(row[1])
        name = (row[0]).replace("_"," ")
        headers.append({'name': name,'type': col_type})
        category_columns.append({'name': name,'type': col_type})

    rows = []
    # get all data/rows from category
    cursor.execute("SELECT * FROM "+subcat_name)
    for row in cursor.fetchall():
        # - save column data from category table
        dict_row = {}
        i = 0
        for column in category_columns:
            dict_row[column['name']] = row[i]
            i += 1
        rows.append(dict_row)
    return {'headers':headers,'rows':rows}


def get_data_from_authors_as_headers_and_column_data(db):
    cursor = db.cursor()
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


def get_subcategory_data(db, subcat_id):
    cursor = db.cursor()
    subcat_name = create_subcategory_name(subcat_id)
    dict_array = []
    cursor.execute("SELECT id, name from "+subcat_name)
    for row in cursor.fetchall():
        dict_array.append({'name': row[1],'id': row[0]})
    return dict_array


def get_data_from_category_as_headers_and_column_data(db, cat_id):
    cursor = db.cursor()
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
    cursor_2 = db.cursor()
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


def set_as_list(string):
    lst = string.split(";")
    return [ r for r in lst if r != '']


def get_values_from_paper_as_dict(db, paper_id):
    cursor = db.cursor()
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


def get_data_from_category_by_cat_id(db, cat_id):
    cursor = db.cursor()
    cursor.execute("select id, name from "+create_category_name(cat_id))
    dict_array = []
    for row in cursor.fetchall():
        dict_array.append({'name':row[1],'id':row[0]})
    return dict_array


def get_paper_id_where_title_exactly(db, title):
    cursor = db.cursor()
    cursor.execute("select id from paper where title=%s",[title])
    for row in cursor.fetchall():
        return row[0]


def delete_row_from_subcategory(db, subcat_id, row_id):
    cursor = db.cursor()
    subcat_table = create_subcategory_name(subcat_id)
    rel_table_list = []
    # delete all relations possible with row_id
    # - get all rel_table names
    cursor.execute("SELECT cat_id, interaction FROM cat_subcat_interactions WHERE subcat_id=%s",[subcat_id])
    for row in cursor.fetchall():
        cat_id = row[0]
        interaction = row[1]
        rel_table_list.append(create_cat_has_subcat_name(cat_id,subcat_id,interaction))
    # - for each rel_table delete relations that contain row_id
    for table in rel_table_list:
        cursor.execute("DELETE FROM "+table+" WHERE "+subcat_table+"_id=%s",[row_id])
    # delete row_id from subcat_table
    cursor.execute("DELETE FROM "+subcat_table+" WHERE id=%s",[row_id])
    # Commit changes in the database
    db.commit()


def delete_row_from_category(db, cat_id, row_id):
    cursor = db.cursor()
    cat_table = create_category_name(cat_id)
    paper_has_cat = create_paper_has_category_name(cat_id)
    # delete all relations possible with row_id
    rel_table_list = []
    # delete all relations possible with row_id
    # - get all rel_table names
    cursor.execute("SELECT subcat_id, interaction FROM cat_subcat_interactions WHERE cat_id=%s",[cat_id])
    for row in cursor.fetchall():
        subcat_id = row[0]
        interaction = row[1]
        rel_table_list.append(create_cat_has_subcat_name(cat_id,subcat_id,interaction))
    # - for each rel_table delete relations that contain row_id
    for table in rel_table_list:
        cursor.execute("DELETE FROM "+table+" WHERE "+cat_table+"_id=%s",[row_id])
    cursor.execute("DELETE FROM "+paper_has_cat+" WHERE "+cat_table+"_id=%s",[row_id])
    # delete row_id from cat_table
    cursor.execute("DELETE FROM "+cat_table+" WHERE id=%s",[row_id])
    # Commit changes in the database
    db.commit()


def search_papers_id(db, paper_values, authors_value, categories_values,show_not_in_selection=False):
    cursor = db.cursor()
    # Search paper ids with paper_values
    where_clause = ""
    values_tuple = ()
    if not show_not_in_selection:
        where_clause = "NOT code_name='not-in-selection' AND "
    # - using the values in paper values create a search string for the 'where' clause
    for value in paper_values:
        where_clause = where_clause+value['id_name']+" like %s AND "
        values_tuple += ("%"+value['value']+"%",)
    where_clause = where_clause[0:len(where_clause)-5]
    cursor.execute("SELECT DISTINCT id FROM paper WHERE "+where_clause, values_tuple)
    # - get all ids and save them as a 'set'
    paper_conditions_id_list = []
    for row in cursor.fetchall():
        paper_conditions_id_list.append(row[0])
    paper_conditions_id_set = Set(paper_conditions_id_list)

    # Search for all the papers with all authors in authors_value
    # - create a list using authors_value string
    authors_list = set_as_list(authors_value)
    # - for each author get a set of paper ids (create a list of sets)
    id_dict_by_author = {}
    for author in authors_list:
        cursor.execute('''SELECT DISTINCT paper_id FROM paper_has_authors WHERE author_id in (SELECT id FROM
        author WHERE name LIKE %s)''', ["%"+author+"%"])
        id_list_by_author = []
        for row in cursor.fetchall():
            id_list_by_author.append(row[0])
        id_dict_by_author[author] = Set(id_list_by_author)

    # Search for all the paper that meet the 'category' specifications
    paper_id_sets_by_category_list = []
    # - for each category in categories_values:
    for category in categories_values:
        cat_id = category['cat_id']
        cat_table_name = create_category_name(cat_id)
        category_where_clause = ""
        category_values_tuple = ()
        # If the table is empty it should not be taken into account in the search
        cursor.execute("SELECT COUNT(id) FROM "+cat_table_name)
        is_this_table_empty = False
        for row in cursor.fetchall():
            if int(row[0]) == 0:
                is_this_table_empty = True
        if is_this_table_empty:
            continue
        # - - get the category_ids that meet the non-subcat specifications as a set
        for element in category['values']:
            if not element['is_subcat']:
                category_where_clause = category_where_clause+element['id_name']+" like %s AND "
                category_values_tuple += ("%"+element['value']+"%",)
        category_where_clause = category_where_clause[0:len(category_where_clause)-5]
        category_id_by_column_conditions_list = []
        cursor.execute('''SELECT DISTINCT id FROM '''+cat_table_name+''' WHERE '''+category_where_clause,
                       category_values_tuple)
        for row in cursor.fetchall():
            category_id_by_column_conditions_list.append(row[0])
        category_id_by_column_conditions_set = Set(category_id_by_column_conditions_list)

        # - - for each subcat get the category_ids that meet the subcat spec. as a set (create a set list)
        category_ids_sets_by_subcategory_condition_list = [] # note that here each element is a set of ids
        for element in category['values']:
            if element['is_subcat']:
                subcat_id = element['subcat_id']
                subcat_name = create_subcategory_name(subcat_id)
                interaction = element['rel_with_cat']
                cat_interact_subcat_table_name = create_cat_has_subcat_name(cat_id, subcat_id, interaction)
                # If the table is empty it should not be taken into account in the search
                cursor.execute("SELECT COUNT("+cat_table_name+"_id) FROM "+cat_interact_subcat_table_name)
                is_this_table_empty = False
                for row in cursor.fetchall():
                    if int(row[0]) == 0:
                        is_this_table_empty = True
                if is_this_table_empty:
                    continue
                # If the table is not empty, proceed
                cursor.execute('''SELECT DISTINCT '''+cat_table_name+'''_id FROM '''+cat_interact_subcat_table_name+
                               ''' WHERE '''+subcat_name+'''_id IN (SELECT id FROM '''+subcat_name
                               +''' WHERE name LIKE %s)''',
                               ["%"+element['name_value']+"%"])
                category_id_list_by_this_subcategory_conditions = []
                for row in cursor.fetchall():
                    category_id_list_by_this_subcategory_conditions.append(row[0])
                category_ids_sets_by_subcategory_condition_list.append(Set(category_id_list_by_this_subcategory_conditions))
        # - - get the intersection of the previous sets as a new set
        for id_set in category_ids_sets_by_subcategory_condition_list:
            category_id_by_column_conditions_set.intersection_update(id_set)
        # - - with the new set search for the papers ids that are relates to this category_ids
        in_string = "("
        for v in category_id_by_column_conditions_set:
            in_string = in_string+str(v)+","
        in_string = in_string[0:len(in_string)-1]+")"
        paper_has_table_name = create_paper_has_category_name(cat_id)
        if len(in_string) > 1:
            cursor.execute("SELECT DISTINCT paper_id FROM "+paper_has_table_name+" WHERE "+
                           cat_table_name+"_id in "+in_string)
        paper_id_list_for_this_category_conditions = []
        for row in cursor.fetchall():
            paper_id_list_for_this_category_conditions.append(row[0])
        # - - create a set of paper_ids with those (append to a list of paper_ids by category)
        paper_id_sets_by_category_list.append(Set(paper_id_list_for_this_category_conditions))
    # Return the intersection of all the paper_id sets and set lists previously created
    for cat_set in paper_id_sets_by_category_list:
        paper_conditions_id_set.intersection_update(cat_set)
    for author in authors_list:
        paper_conditions_id_set.intersection_update(id_dict_by_author[author])

    str_in = "("
    for el in list(paper_conditions_id_set):
        str_in = str_in + str(el) + ","
    str_in = str_in[0:len(str_in)-1]+")"
    if len(str_in) > 1:
        cursor.execute("SELECT id FROM paper WHERE id IN "+str_in+" ORDER BY year")
        result_id_list = []
        for row in cursor.fetchall():
            result_id_list.append(row[0])
        return result_id_list
    else:
        return list(paper_conditions_id_set)


def add_author(db, author_name, author_affiliation):
    cursor = db.cursor()
    cursor.execute("INSERT INTO author (name, affiliation) values (%s,%s)",(author_name,author_affiliation))
    # Commit changes in the database
    db.commit()


def modify_author(db, author_id, author_name, author_affiliation):
    cursor = db.cursor()
    cursor.execute("UPDATE author SET name=%s, affiliation=%s WHERE id=%s",(author_name, author_affiliation, author_id))
    # Commit changes in the database
    db.commit()


def delete_row_from_author(db, author_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM paper_has_authors WHERE author_id=%s",[author_id])
    cursor.execute("DELETE FROM author WHERE id=%s",[author_id])
    # Commit changes in the database
    db.commit()


def create_interaction_for_existing_subcategory(db,cat_id,interaction, subcat_id):
    cursor = db.cursor()
    subcategory_name = create_subcategory_name(subcat_id)
    # insert interaction on cat_subcat_interactions
    cursor.execute("INSERT INTO cat_subcat_interactions (cat_id,interaction,subcat_id) VALUES (%s,%s,%s)",
                   (cat_id,interaction,subcat_id))
    # create cat_interaction_subcat table
    interaction_table_name = create_cat_has_subcat_name(cat_id,subcat_id,interaction)
    category_name = create_category_name(cat_id)
    create_relation_table = '''CREATE TABLE '''+interaction_table_name+'''('''+category_name+'''_id MEDIUMINT,'''+\
                            subcategory_name+'''_id MEDIUMINT,
    FOREIGN KEY ('''+category_name+'''_id) REFERENCES '''+category_name+'''(id), FOREIGN KEY ('''+\
                            subcategory_name+'''_id) REFERENCES '''+subcategory_name+'''(id))'''
    cursor.execute(create_relation_table)
    # Commit changes in the database
    db.commit()


def parse_type(type_name):
    if 'int' in type_name:
        return 'number'
    if 'varchar' in type_name:
        return 'varchar'
    if 'text' in type_name:
        return 'text'
    else:
        return 'varchar'


def unparse_type(type_name):
    if 'number' == type_name:
        return 'mediumint'
    if 'varchar' == type_name:
        return 'varchar(100)'
    if 'text' in type_name:
        return 'text'


def get_columns_data_types():
    return ['varchar', 'number', 'text']


def get_category_name_from_id(db, cat_id):
    cursor = db.cursor()
    cursor.execute("SELECT name FROM categories WHERE id=%s",[cat_id])
    for row in cursor.fetchall():
        return row[0]

