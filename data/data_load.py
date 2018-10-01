import psycopg2
from credentials import DatabaseCredentials as dbc
from jumbo_load import jumbo_load

# connection to the database
# TODO: read params from separate file
connection = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(dbc.dbname, dbc.user, dbc.host, dbc.password))

# cursor to perform database operations
cursor = connection.cursor()

# LET'S FIRST CREATE THE SCHEMA
print('creating schemas..')
cursor.execute(open("schema.sql", "r").read())

# NOW WE'LL ADD THE DATA
print('inserting countries..')
cursor.execute(open("countries.sql", "r").read())

print('inserting ratings..')
cursor.execute(open("ratings.sql", "r").read())

print('inserting languages..')
cursor.execute(open("languages.sql", "r").read())

print('inserting genres..')
cursor.execute(open("genres.sql", "r").read())

print('inserting movies, people and roles...')
jumbo_load(cursor)

# make the changes to the database persistent
connection.commit()

# close communication with the database
cursor.close()
connection.close()