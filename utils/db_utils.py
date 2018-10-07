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
        query = sql.SQL("SELECT * FROM person WHERE name={0};").format(
            sql.Literal(name)
        )
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def print_query(self, query):
        # just for debugging
        print("----------------------------------------------")
        print(self.cursor.mogrify(query))
        print("----------------------------------------------")

    def insert_person(self, name, dob=None):
        if dob:
            query = sql.SQL("""INSERT INTO person ("name", "dob") VALUES ({}, {});""").format(
                sql.Literal(name), sql.Literal(dob)
            )
        else:
            query = sql.SQL("""INSERT INTO person ("name") VALUES ({});""").format(
                sql.Literal(name)
            )
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

    def get_movies(self, filters, page_number=1, page_size=20):
        limit = page_size
        offset = page_size * (page_number - 1)

        conditions = list()
        if "title" in filters:
            conditions.append(sql.SQL("title ilike {0} ").format(sql.Literal('%' + filters["title"] + '%')))
        if "company" in filters:
            conditions.append(sql.SQL("company ilike {0} ").format(sql.Literal('%' + filters["company"] + '%')))

        # let's first get the counts
        query = sql.SQL("SELECT count(*) FROM movie WHERE {0};").format(
            sql.SQL(" and ").join(conditions)
        )
        self.cursor.execute(query)
        total_hits = self.cursor.fetchone()[0]

        # now let's get the actual movies in the limit
        query = sql.SQL("SELECT * FROM movie WHERE {0} LIMIT {1} OFFSET {2};").format(
            sql.SQL(" and ").join(conditions), sql.Literal(limit), sql.Literal(offset)
        )
        self.cursor.execute(query)

        return {
            "values": self.cursor.fetchall(),
            "pagination": {
                "page_number": page_number,
                "page_size": page_size,
                "total_hits": total_hits,
                "total_pages": total_hits // page_size + 1
            }
        }

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
