import csv
import ast
import sys
import os.path
from utils.db_utils import DatabaseUtils, MockCursor

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))


def jumbo_load():
    count = 0
    max_count = 100
    db_utils = DatabaseUtils()
    with open("movies.csv", errors='ignore') as f1:
        with open("movies_with_omdb.csv", errors='ignore') as f2:
            rows = zip(csv.reader(f1), csv.reader(f2))
            headers = next(rows)
            for basic, omdb_row in rows:
                omdb = ast.literal_eval(omdb_row[2])
                if omdb["Response"] == "False":
                    continue
                # we have a clean 'row'

                # PEOPLE
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

                # ROLES
                director_role = db_utils.get_personal_role(db_director, "Director")
                actor_role = db_utils.get_personal_role(db_actor, "Actor")
                writer_role = db_utils.get_personal_role(db_writer, "Writer")

                if not director_role:
                    db_utils.insert_role(db_director, "Director")
                if not actor_role:
                    db_utils.insert_role(db_actor, "Actor")
                if not writer_role:
                    db_utils.insert_role(db_writer, "Writer")

                # MOVIE
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

                # INVOLVEMENT
                director_involvement = db_utils.get_involvement(db_director, movie, "Director")
                actor_involvement = db_utils.get_involvement(db_actor, movie, "Actor")
                writer_involvement = db_utils.get_involvement(db_writer, movie, "Writer")

                if not director_involvement:
                    db_utils.insert_involvement(db_director, movie, "Director")

                if not actor_involvement:
                    db_utils.insert_involvement(db_actor, movie, "Actor")

                if not writer_involvement:
                    db_utils.insert_involvement(db_writer, movie, "Writer")

                db_utils.commit()

                count += 1
                print("DONE " + str(count))
                if count >= max_count:
                    break


if __name__ == "__main__":
    jumbo_load(MockCursor())
