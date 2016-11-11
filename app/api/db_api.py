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
    create_category_table = '''CREATE TABLE '''+cat_name+'''(id MEDIUMINT NOT NULL AUTO_INCREMENT primary key)'''
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
    (id MEDIUMINT NOT NULL AUTO_INCREMENT primary key)'''
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


def parse_type(type_name):
    if 'int' in type_name:
        return 'number'
    if 'varchar' in type_name:
        return 'varchar'
    if 'text' in type_name:
        return 'text'


def unparse_type(type_name):
    if 'number' == type_name:
        return 'mediumint'
    if 'varchar' == type_name:
        return 'varchar(100)'
    if 'text' in type_name:
        return 'text'


def get_columns_data_types():
    return ['varchar', 'number', 'text']

