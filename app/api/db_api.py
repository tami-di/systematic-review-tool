__author__ = 'ivana'
import MySQLdb
from db_config import db_config


def connect_db():
    db = MySQLdb.connect(host=db_config['host'], user=db_config['user'],
                         passwd=db_config['passwd'], db=db_config['db'])
    return db


def create_category_name(category_id):
    return "cat"+str(category_id)


def create_category_table_name(category_id):
    return "paper_has_"+create_category_name(category_id)


def create_category(db,name, description):
    cursor = db.cursor()
    cursor.execute('''INSERT into categories (name, description)
                  values (%s, %s)''', (name, description))
    cursor.execute("SELECT id FROM categories WHERE name = %s", [name])
    category_id = ""
    for row in cursor.fetchall():
        category_id = row[0]
        break
    # make the in-database name of table and category
    cat_name = create_category_name(category_id)
    cat_table_name = create_category_table_name(category_id)

    # command to create table, columns haven't been decided yet
    create_category_table = '''CREATE TABLE '''+cat_table_name+'''(id MEDIUMINT NOT NULL AUTO_INCREMENT primary key)'''
    # command to create relacional table between the category table and the paper
    create_paper_has = '''CREATE TABLE paper_has_'''+cat_name+'''(paper_id MEDIUMINT,'''+cat_name+'''_id MEDIUMINT,
    FOREIGN KEY (paper_id) REFERENCES paper(id), FOREIGN KEY ('''+cat_name+'''_id) REFERENCES '''+cat_table_name+'''
    (id))'''
    # command execution
    cursor.execute(create_category_table)
    cursor.execute(create_paper_has)
    # Commit your changes in the database
    db.commit()

