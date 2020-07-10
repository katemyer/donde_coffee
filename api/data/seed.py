# https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
#https://stackoverflow.com/questions/14257373/skip-the-headers-when-editing-a-csv-file-using-python
#to drop a table: https://www.tutorialspoint.com/python_data_access/python_sqlite_drop_table.htm

import csv, sqlite3, os
from sqlite3 import Error

# https://stackoverflow.com/questions/918154/relative-paths-in-python
dirname = os.path.dirname(__file__)
database = os.path.join(dirname, "../database.db")
user_csv = os.path.join(dirname, "user.csv")

conn = sqlite3.connect(database)
curs = conn.cursor()

#drop table
table_name = """DROP TABLE IF EXISTS User""" #actual sql command for if statement
curs.execute(table_name) #actually execute command

table_shop_name = """DROP TABLE IF EXISTS Shop""" #actual sql command for if statement
curs.execute(table_shop_name) #actually execute command

#create table
#name text NOT NULL means required field
create_table_sql = """ CREATE TABLE IF NOT EXISTS User (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL, 
                                        email text
                                    ); """

create_shop_table_sql = """ CREATE TABLE IF NOT EXISTS Shop (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL, 
                                        address text,
                                        hours text
                                    ); """

curs.execute(create_table_sql)
curs.execute(create_shop_table_sql)

reader = csv.reader(open(user_csv, 'r'), delimiter=',')
next(reader, None)  # skip the headers
for row in reader:
    to_db = [row[0], row[1]] #2 columns
    curs.execute("INSERT INTO User (name, email) VALUES (?, ?);", to_db)

conn.commit()
conn.close()