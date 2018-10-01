import csv
import json
import ast

def test_omdb_data_integrity():
    count_rows = 0
    count_movie_okay = 0
    count_movie_not_found = 0
    with open("movies_with_omdb.csv") as f:
        reader = csv.reader(f)
        headers = next(reader)
        for row in reader:
            assert(len(row) == 3)
            omdb_data = ast.literal_eval(row[2])
            count_rows += 1
            if omdb_data["Response"] == "True":
                assert(len(omdb_data.keys()) == 25)
                count_movie_okay += 1
            else:
                assert(omdb_data["Error"] == "Movie not found!")
                count_movie_not_found += 1
    print("Verified {} entries. OMDB matched {} movies. {} movies not found in their db.".format(
        count_rows, count_movie_okay, count_movie_not_found
    ))

def test_movie_order_in_two_files():
    with open("movies.csv") as f1:
        with open("movies_with_omdb.csv") as f2:
            rows = zip(csv.reader(f1), csv.reader(f2))
            headers = next(rows)
            for row1, row2 in rows:
                assert(row1[6] == row2[0])
                assert(row1[14] == row2[1])

def get_countries():
    countries = set()
    with open("movies.csv") as f1:
        with open("movies_with_omdb.csv") as f2:
            rows = zip(csv.reader(f1), csv.reader(f2))
            headers = next(rows)
            for row1, row2 in rows:
                omdb_data = ast.literal_eval(row2[2])
                if omdb_data["Response"] == "False":
                    continue
                countries.add(row1[2].strip())
                for c in omdb_data["Country"].split(','):
                    countries.add(c.strip())
    countries = sorted(countries)

    with open("countries.sql", "w") as file:
        for country in countries:
            file.write("""INSERT INTO country ("name") VALUES ('{}');\n""".format(country))

def get_mpaa_ratings():
    mpaa_ratings = set()
    with open("movies.csv") as f1:
        with open("movies_with_omdb.csv") as f2:
            rows = zip(csv.reader(f1), csv.reader(f2))
            headers = next(rows)
            for row1, row2 in rows:
                omdb_data = ast.literal_eval(row2[2])
                if omdb_data["Response"] == "False":
                    continue
                mpaa_ratings.add(row1[7].strip())
                for c in omdb_data["Rated"].split(','):
                    mpaa_ratings.add(c.strip())
    mpaa_ratings = sorted(mpaa_ratings)

    unrated_equivalents = ["N/A", "NOT RATED", "Not specified"]
    for x in unrated_equivalents:
        if x in mpaa_ratings:
            mpaa_ratings.remove(x)

    with open("ratings.sql", "w") as file:
        for mpaa_rating in mpaa_ratings:
            file.write("""INSERT INTO rating ("name") VALUES ('{}');\n""".format(mpaa_rating))
        file.write("\n-- {} are all replaced with UNRATED\n".format(unrated_equivalents))

def get_languages():
    languages = set()
    with open("movies.csv") as f1:
        with open("movies_with_omdb.csv") as f2:
            rows = zip(csv.reader(f1), csv.reader(f2))
            headers = next(rows)
            for row1, row2 in rows:
                omdb_data = ast.literal_eval(row2[2])
                if omdb_data["Response"] == "False":
                    continue
                for c in omdb_data["Language"].split(','):
                    languages.add(c.strip())
    languages = sorted(languages)

    with open("languages.sql", "w") as file:
        for language in languages:
            file.write("""INSERT INTO language ("name") VALUES ('{}');\n""".format(language))

def get_genres():
    genres = set()
    with open("movies.csv") as f1:
        with open("movies_with_omdb.csv") as f2:
            rows = zip(csv.reader(f1), csv.reader(f2))
            headers = next(rows)
            for row1, row2 in rows:
                omdb_data = ast.literal_eval(row2[2])
                if omdb_data["Response"] == "False":
                    continue
                genres.add(row1[4].strip())
                for c in omdb_data["Genre"].split(','):
                    genres.add(c.strip())
    genres = sorted(genres)

    with open("genres.sql", "w") as file:
        for genre in genres:
            file.write("""INSERT INTO genre ("name") VALUES ('{}');\n""".format(genre))

if __name__=='__main__':
    test_omdb_data_integrity()
    test_movie_order_in_two_files()
    get_countries()
    get_mpaa_ratings()
    get_languages()
    get_genres()