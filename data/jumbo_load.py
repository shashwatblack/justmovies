import csv
import ast

from utils import DatabaseUtils, MockCursor

def jumbo_load(cursor):
    c = 0
    mx_c = 100
    db_utils = DatabaseUtils(cursor)
    with open("movies.csv", errors='ignore') as f1:
        with open("movies_with_omdb.csv", errors='ignore') as f2:
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
                    db_director = db_utils.insert_then_get_person(director)
                if not db_actor:
                    db_actor = db_utils.insert_then_get_person(actor)
                if not db_writer:
                    db_writer = db_utils.insert_then_get_person(writer)

                director_role = db_utils.get_personal_role(db_director, "Director")
                actor_role = db_utils.get_personal_role(db_actor, "Actor")
                writer_role = db_utils.get_personal_role(db_writer, "Writer")

                if not director_role:
                    db_utils.insert_role(db_director, "Director")
                if not actor_role:
                    db_utils.insert_role(db_actor, "Actor")
                if not writer_role:
                    db_utils.insert_role(db_writer, "Writer")

                title = basic[6]
                year = basic[14]
                movie = db_utils.get_movie(title, year)
                if not movie:
                    movie = db_utils.insert_then_get_movie(title, year, {
                        "company": basic[1],
                        "budget": basic[0],
                        "gross": basic[5],
                        "released": basic[8],
                        "runtime": basic[9],
                        "plot": omdb["Plot"],
                        "awards": omdb["Awards"],
                        "poster": omdb["Poster"],
                        "website": omdb["Website"],
                        "imdb_rating": omdb["imdbRating"],
                        "imdb_id": omdb["imdbID"],

                        # genre
                        # mpaa_rating
                        # country
                        # language
                    })

                # if no involvement
                    # insert involvement

                c += 1
                if c >= mx_c:
                    break


if __name__=="__main__":
    jumbo_load(MockCursor())
