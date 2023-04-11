__author__ = 'ivana'

def show_columns(db,table_name):
    cursor = db.connection.cursor()
    cursor.execute("SHOW COLUMNS FROM "+table_name)
    return cursor.fetchall()
    

def show_columns_of_category(db,cat_id):
    cursor = db.connection.cursor()
    columns=show_columns(db,"categories")
    columns=columns[:-1]
