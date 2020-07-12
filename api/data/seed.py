# https://stackoverflow.com/questions/2887878/importing-a-csv-file-into-a-sqlite3-database-table-using-python
#https://stackoverflow.com/questions/14257373/skip-the-headers-when-editing-a-csv-file-using-python
#to drop a table: https://www.tutorialspoint.com/python_data_access/python_sqlite_drop_table.htm

import csv, sqlite3, os
from sqlite3 import Error

# https://stackoverflow.com/questions/918154/relative-paths-in-python
dirname = os.path.dirname(__file__)
database = os.path.join(dirname, "../database.db")
users_csv = os.path.join(dirname, "users.csv")
shops_csv = os.path.join(dirname, "shops.csv")

conn = sqlite3.connect(database)
curs = conn.cursor()

#drop table
table_name = """DROP TABLE IF EXISTS users""" #actual sql command for if statement
curs.execute(table_name) #actually execute command

table_shop_name = """DROP TABLE IF EXISTS shops""" #actual sql command for if statement
curs.execute(table_shop_name) #actually execute command

#create table
#name text NOT NULL means required field
create_users_table_sql = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL, 
                                        email text,
                                        password text
                                    ); """

create_shop_table_sql = """ CREATE TABLE IF NOT EXISTS shops (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL, 
                                        description text,
                                        hours text,
                                        address text,
                                        phone text,
                                        website text,
                                        price_level text
                                    ); """

curs.execute(create_users_table_sql)
curs.execute(create_shop_table_sql)

reader = csv.reader(open(users_csv, 'r'), delimiter=',')
next(reader, None)  # skip the headers
for row in reader:
    to_db = [row[0], row[1]] #2 columns
    curs.execute("INSERT INTO users (name, email) VALUES (?, ?);", to_db)

reader = csv.reader(open(shops_csv, 'r'), delimiter=',')
next(reader, None)  # skip the headers
for row in reader:
    to_db = [row[0], row[1],row[2],row[3],row[4],row[5],row[6]] #2 columns
    curs.execute("INSERT INTO shops (name, description, hours, address, phone, website, price_level) VALUES (?, ?, ?, ?, ?, ?, ?);", to_db)

conn.commit()
conn.close()