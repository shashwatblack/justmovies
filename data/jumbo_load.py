import csv
import ast

from utils import DatabaseUtils, MockCursor

def jumbo_load(cursor):
    c = 0
    mx_c = 100
    db_utils = DatabaseUtils(cursor)
    with open("movies.csv") as f1:
        with open("movies_with_omdb.csv") as f2:
            rows = zip(csv.reader(f1), csv.reader(f2))
            headers = next(rows)
            for basic, omdb_row in rows:
                omdb = ast.literal_eval(omdb_row[2])
                if omdb["Response"] == "False":
                    continue
                # we have a clean 'row'

                director = basic[3]
                actor = basic[11]
                writer = basic[13]

                db_director = db_utils.get_person(director)
                db_actor = db_utils.get_person(actor)
                db_writer = db_utils.get_person(writer)

                if not db_director:
                    db_utils.insert_person(director)
                if not db_actor:
                    db_utils.insert_person(actor)
                if not db_writer:
                    db_utils.insert_person(writer)

                # if no actor.personal_role
                    # insert personal_role
                # if no movie
                    # insert movie
                # if no involvement
                    # insert involvement

                c += 1
                if c >= mx_c:
                    break


if __name__=="__main__":
    jumbo_load(MockCursor())
