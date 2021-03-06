import psycopg2
from psycopg2 import sql
import sys
import os.path
from utils.credentials import DatabaseCredentials as dbc

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))


class DatabaseUtils():
    cursor = None
    connection = None
    genres = []
    mpaa_ratings = []
    countries = []
    languages = []

    # CONSTRUCTOR
    def __init__(self):
        self.connection = psycopg2.connect("dbname='{0}' user='{1}' host='{2}' password='{3}'".format(dbc.dbname, dbc.user, dbc.host, dbc.password))
        self.connection.set_client_encoding('UNICODE')

        # cursor to perform database operations
        self.cursor = self.connection.cursor()

        self.fetch_enums()

    # DESTRUCTOR
    def __del__(self):
        # close communication with the database
        self.cursor.close()
        self.connection.close()

    # MISC
    def commit(self):
        # make the changes to the database persistent
        self.connection.commit()

    def get_cursor(self):
        return self.cursor

    def get_connection(self):
        return self.connection

    def print_query(self, query):
        # just for debugging
        print("----------------------------------------------")
        print(self.cursor.mogrify(query))
        print("----------------------------------------------")

    def fetch_enums(self):
        # genres
        self.cursor.execute("SELECT * FROM genre;")
        self.genres = self.cursor.fetchall()

        # mpaa_ratings
        self.cursor.execute("SELECT * FROM rating;")
        self.mpaa_ratings = self.cursor.fetchall()

        # countries
        self.cursor.execute("SELECT * FROM country;")
        self.countries = self.cursor.fetchall()

        # languages
        self.cursor.execute("SELECT * FROM language;")
        self.languages = self.cursor.fetchall()

    # PEOPLE
    def get_person(self, name):
        query = sql.SQL("SELECT * FROM person WHERE name={0};").format(
            sql.Literal(name)
        )
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_people(self, name):
        query = sql.SQL("SELECT * FROM person WHERE name ilike {0};").format(
            sql.Literal("%" + name + "%")
        )
        self.cursor.execute(query)
        return self.cursor.fetchall()

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

    # PERSONAL ROLES
    def get_personal_role(self, person_pk, role):
        if isinstance(person_pk, tuple):
            person_pk = person_pk[0]
        query = """SELECT * FROM personal_role WHERE person='{}' and role='{}';""".format(person_pk, role)
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_personal_roles(self, person_pk):
        if isinstance(person_pk, tuple):
            person_pk = person_pk[0]
        query = """SELECT * FROM personal_role WHERE person='{}';""".format(person_pk)
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert_role(self, person_pk, role):
        if isinstance(person_pk, tuple):
            person_pk = person_pk[0]
        query = """INSERT INTO personal_role ("person", "role") VALUES ('{}', '{}');""".format(person_pk, role)
        self.cursor.execute(query)

    # MOVIES
    def get_movie(self, title, year):
        query = """SELECT * FROM movie WHERE title=%s and year=%s;"""
        self.cursor.execute(query, (title, year))
        return self.cursor.fetchone()

    def get_movie_from_pk(self, movie_pk):
        query = """SELECT * FROM movie WHERE pk=%s;"""
        self.cursor.execute(query, (movie_pk,))
        return self.cursor.fetchone()

    def get_movies(self, filters, page_number=1, page_size=20):
        limit = page_size
        offset = page_size * (page_number - 1)

        conditions = [sql.SQL("True")]
        if "title" in filters and len(filters["title"]):
            conditions.append(sql.SQL("title ilike {0} ").format(sql.Literal('%' + filters["title"] + '%')))
        if "company" in filters and len(filters["company"]):
            conditions.append(sql.SQL("company ilike {0} ").format(sql.Literal('%' + filters["company"] + '%')))
        if "year_gte" in filters and len(filters["year_gte"]):
            conditions.append(sql.SQL("year >= {0} ").format(sql.Literal(filters["year_gte"])))
        if "year_lte" in filters and len(filters["year_lte"]):
            conditions.append(sql.SQL("year <= {0} ").format(sql.Literal(filters["year_lte"])))
        if "imdb_rating" in filters and len(filters["imdb_rating"]):
            conditions.append(sql.SQL("imdb_rating >= {0} ").format(sql.Literal(filters["imdb_rating"])))

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

    def update_movie(self, movie_pk, params={}):
        query = sql.SQL("UPDATE movie SET {0} WHERE pk={1};").format(
            sql.SQL(', ').join([sql.Identifier(key) + sql.SQL('=') + sql.Literal(params[key]) for key in params]),
            sql.Literal(movie_pk)
        )
        self.cursor.execute(query)
        self.commit()

    def delete_movie(self, movie_pk):
        query = sql.SQL("DELETE FROM movie WHERE pk={0};").format(
            sql.Literal(movie_pk)
        )
        self.cursor.execute(query)
        self.commit()

    # INVOLVEMENTS
    def get_involvement(self, person_pk, movie_pk, role):
        if isinstance(person_pk, tuple):
            person_pk = person_pk[0]
        if isinstance(movie_pk, tuple):
            movie_pk = movie_pk[0]
        query = sql.SQL("SELECT * FROM involvement WHERE person={} and movie={} and role={};").format(
            sql.Literal(person_pk), sql.Literal(movie_pk), sql.Literal(role)
        )
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def insert_involvement(self, person_pk, movie_pk, role):
        if isinstance(person_pk, tuple):
            person_pk = person_pk[0]
        if isinstance(movie_pk, tuple):
            movie_pk = movie_pk[0]
        query = sql.SQL("""INSERT INTO involvement ("person", "movie", "role") VALUES ({}, {}, {});""").format(
            sql.Literal(person_pk), sql.Literal(movie_pk), sql.Literal(role)
        )
        self.cursor.execute(query)

    def get_involvements(self, person_pk):
        if isinstance(person_pk, tuple):
            person_pk = person_pk[0]
        query = sql.SQL("""SELECT * FROM movie NATURAL JOIN involvement WHERE involvement.person={};""").format(
            sql.Literal(person_pk)
        )
        self.cursor.execute(query)

        return self.cursor.fetchall()

    # GENRES
    def get_genre(self, genre):
        match = filter(lambda x: x[1] == genre, self.genres)
        return next(match) if match else None

    # MPAA RATINGS
    def get_mpaa_rating(self, mpaa_rating):
        if mpaa_rating in ['N/A', 'NOT RATED', 'Not specified']:
            mpaa_rating = "UNRATED"
        match = filter(lambda x: x[1] == mpaa_rating, self.mpaa_ratings)
        return next(match) if match else None

    # COUNTRIES
    def get_country(self, country):
        match = filter(lambda x: x[1] == country, self.countries)
        return next(match) if match else None

    # LANGUAGES
    def get_language(self, language):
        match = filter(lambda x: x[1] == language, self.languages)
        return next(match) if match else None


class MockCursor:
    def execute(self, query):
        print("EXECUTING", query)

    def fetchone(self):
        print("FETCH-ONE")
        return {}
