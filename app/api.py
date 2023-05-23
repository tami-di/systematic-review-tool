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
    

#-------------------------Functions for Index---------------------------

""" Funtion for"""
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

""" Funtion for"""
def get_data_from_category_by_cat_id(db, cat_id):
    cursor = db.connection.cursor()
    #select the content that is related to the category
    cursor.execute("SELECT id, name FROM content WHERE id IN (SELECT cont_id FROM cat_cont WHERE cat_id="+str(cat_id)+")")
    dict_array = []
    for row in cursor.fetchall():
        dict_array.append({'name':row[1],'id':row[0]})
    return dict_array