__author__ = 'ivana'


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
    create_relation_table = '''CREATE TABLE '''+paper_has_cat_name+'''(paper_id MEDIUMINT,'''+cat_name+'''_id MEDIUMINT,
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
        dict_array.append({'name':subcat_name,'id':subcat_id,'properties':properties, 'properties_type':properties_type,
                           'type':type,'is_subcat':is_subcat})
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
        dict_array.append({'name':str(row[1]).replace("_"," "),'type':'category','data':data,'id':row[0]})
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
            " where paper_id = "+ paper_id +")")
    for row in cursor.fetchall():
        value.append(row[0])
    return value


def add_paper_using_dict_array(db, dict_array):
    cursor = db.cursor()
    title = ""
    library = ""
    code_name = ""
    year = ""
    abstract = ""
    summary = ""
    authors_list = []
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
    for category in categories:
        for value in category['values']:
            cursor.execute("insert into "+category['table_name']+" (paper_id,"+category['cat_name']+
                           "_id) values (%s,%s)",(paper_id,value))
    # Commit changes in the database
    db.commit()


def add_authors_to_paper(db, paper_id, authors):
    cursor = db.cursor()
    for author in authors:
        id = get_author_id_from_name(db,author)
        cursor.execute("insert into paper_has_authors (paper_id, author_id) values (%s, %s)", (paper_id,id))
    # Commit changes in the database
    db.commit()


def set_as_list(string):
    return string.split(";")


def get_values_from_paper_as_dict(db, paper_id):
    cursor = db.cursor()
    dict = {}
    cursor.execute("select title, library, code_name, year, abstract, summary  from paper where id=%s",paper_id)
    for row in cursor.fetchall():
        dict['title'] = row[0]
        dict['library'] = row[1]
        dict['code name'] = row[2]
        dict['year'] = row[3]
        dict['abstract'] = row[4]
        dict['summary'] = row[5]
        break
    return dict

def get_data_from_category_by_cat_id(db, cat_id):
    cursor = db.cursor()
    cursor.execute("select id, name from "+create_category_name(cat_id))
    dict_array = []
    for row in cursor.fetchall():
        dict_array.append({'name':str(row[1]).replace("_"," "),'id':row[0]})
    return dict_array


def get_paper_id_where_title_exactly(db, title):
    cursor = db.cursor()
    cursor.execute("select id from paper where title=%s",[title])
    for row in cursor.fetchall():
        return row[0]


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

