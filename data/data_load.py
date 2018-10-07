import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from utils.db_utils import DatabaseUtils
from jumbo_load import jumbo_load

# connection to the database
db_utils = DatabaseUtils()
connection = db_utils.get_connection()
cursor = db_utils.get_cursor()

# LET'S FIRST CREATE THE SCHEMA
print('creating schemas..')
cursor.execute(open("schema.sql", "r").read())
db_utils.commit()

# NOW WE'LL ADD THE DATA
print('inserting countries..')
cursor.execute(open("countries.sql", "r").read())
db_utils.commit()

print('inserting ratings..')
cursor.execute(open("ratings.sql", "r").read())
db_utils.commit()

print('inserting languages..')
cursor.execute(open("languages.sql", "r").read())
db_utils.commit()

print('inserting genres..')
cursor.execute(open("genres.sql", "r").read())
db_utils.commit()

print('inserting movies, people and roles...')
jumbo_load()

print("done!")
