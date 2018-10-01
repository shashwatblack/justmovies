import csv
import ast

def jumbo_load(cursor):
    with open("movies.csv") as f1:
        with open("movies_with_omdb.csv") as f2:
            rows = zip(csv.reader(f1), csv.reader(f2))
            headers = next(rows)
            for basic, omdb_row in rows:
                omdb = ast.literal_eval(omdb_row[2])
                if omdb["Response"] == "False":
                    continue
                # we have a clean 'row'
                # if no actor:
                	# insert actor
                # if no actor.personal_role
                	# insert personal_role
                # if no movie
	                # insert movie
                # if no involvement
                	# insert involvement 