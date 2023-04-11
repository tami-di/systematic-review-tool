# Systematic review tool

This tool has been developed to assist a systematic review or a paper qualitative data analysis. The tool allows to:
* Add papers to a database
* Create, modify or delete categories
* Add, delete or modify classifications of these categories
* Group classifications into a broader set within the category they belong to (called metacategories)
* Classify papers according to the classifications of each category
* Search papers filtering by any data available about it (incluiding categories, metacategories and their descriptions)
* Search papers obtaining only the pieces of information wanted

This is the first version in Python3 of this tool and it may contain bugs.

## Mode of use:
* Install flask and flask_mysqldb libraries 2.
* Upload the DB found in the DB.sql file to a server.
* Change db_config.py file with your DB information.
* In the terminal run the following command: python -m flask --app app/app run  
* From your browser enter to localhost:5000

## Warnings for use:
* Search engines are case sensitive.
* In the first search engine you must add the exact name

## Dependencies:
 * flask
 * flask_mysqldb
 * MySQL 
