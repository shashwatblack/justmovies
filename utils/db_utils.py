import psycopg2
from psycopg2 import sql

import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from utils.credentials import DatabaseCredentials as dbc

class DatabaseUtils():
    cursor = None
    connection = None

    def __init__(self):
        self.connection = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(dbc.dbname, dbc.user, dbc.host, dbc.password))
        self.connection.set_client_encoding('UNICODE')

        # cursor to perform database operations
        self.cursor = self.connection.cursor()

    def __del__(self):
        print(str(self), 'died')
        # close communication with the database
        self.cursor.close()
        self.connection.close()

    def commit(self):
        # make the changes to the database persistent
        self.connection.commit()

    def get_cursor(self):
        return self.cursor

    def get_connection(self):
        return self.connection

    def get_person(self, name):
        query = """SELECT * FROM person WHERE name='{}';""".format(name)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def insert_person(self, name, dob=None):
        if dob:
            query = """INSERT INTO person ("name", "dob") VALUES ('{}', '{}');""".format(name, dob)
        else:
            query = """INSERT INTO person ("name") VALUES ('{}');""".format(name)
        self.cursor.execute(query)

    def insert_then_get_person(self, name, dob=None):
        self.insert_person(name, dob)
        return self.get_person(name)

    def get_personal_role(self, person_pk, role):
        if isinstance(person_pk, tuple):
            person_pk = person_pk[0]
        query = """SELECT * FROM personal_role WHERE person='{}' and role='{}';""".format(person_pk, role)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def insert_role(self, person_pk, role):
        if isinstance(person_pk, tuple):
            person_pk = person_pk[0]
        query = """INSERT INTO personal_role ("person", "role") VALUES ('{}', '{}');""".format(person_pk, role)
        self.cursor.execute(query)

    def get_movie(self, title, year):
        query = """SELECT * FROM movie WHERE title=%s and year=%s;"""
        self.cursor.execute(query, (title, year))
        return self.cursor.fetchone()

    def insert_movie(self, title, year, params={}):
        params["title"] = title
        params["year"] = year

        query = sql.SQL("INSERT INTO movie ({0}) VALUES ({1});").format(
            sql.SQL(', ').join([sql.Identifier(value) for value in params.keys()]),
            sql.SQL(', ').join([sql.Literal(value) for value in params.values()])
        )
        self.cursor.execute(query)

    def insert_then_get_movie(self, title, year, params={}):
        self.insert_movie(title, year, params)
        return self.get_movie(title, year)


class MockCursor():
    def execute(self, query):
        print("EXECUTING", query)

    def fetchone(self):
        print("FETCH-ONE")
        return {}
