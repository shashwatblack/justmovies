
# JUST MOVIES

## What is it?

Just Movies is a simple movie and celebrity directory. The cherry on the cake is the `data` feature, which runs analytical queries on the available data set and presents them in beautiful charts.

This work is done as a course project for Database Systems (TAMU CSCE 608). The author is Shashwat Shashi Mehta. UIN: **827008698**

## What are its features?
 1. Just Movies
	- Grid of movie posters and names
	- Paginated 20 per page
	- Ability to apply following filters
		- Title (supports substring search)
		- Company (supports substring search)
		- Year (supports ranges `from`-`to`)
		- IMDB Rating
	- Link to IMDB page under each movie poster
	- Link to edit page
 2. Just People
	- Search any celebrity by their name (supports substring search)
	- Will show data for the best match
	- Date of Birth, Roles, Introduction, and Filmography
 3. Just Data
	- Lots of beautiful and insightful charts
	- General bird's-eye view stats
		- Total # of movies in system
		- Total # of celebrities in system
		- Total budget of all movies
		- Total reviews received (Note: `Reviews` feature hasn't been developed yet)
	- Pie Charts
		- Movie count distribution by genre
		- Movie count distribution by country
		- Movie count distribution by language
		- Movie budget distribution by genre
		- Movie budget distribution by country
		- Movie budget distribution by language
	- Celebrity Stats
		- Top 10 celebrities involved in at least 10 movies.
			- The ranking is based on average imdb rating for each of the movies they worked in.
		- Celebrity Role Distribution Venn Diagram
			- How many actors+writers are there?
			- Is writer+director role more common than actor+director?
 4. Movie Edit
	- Edit any of the movie's fields
	- Fixed fields are provided as select dropdown
	- Ability to delete the movie entirely from the system.
		- This will also delete all the associated celebrity involvements and reviews from the system.

## How was the data collected?
 1. The initial data was downloaded from kaggle - https://www.kaggle.com/danielgrijalvas/movies
 2. Additional data, such as posters, imdb id and so on were fetched using the OMDB API - omdbapi.com
 3. A python script `omdb_fetch.py` was written to fetch data in batches over a period of few days (due to API limitations).
 4. All the data was collected in two CSVs - `data/movies.csv` and `data/movies_with_omdb.csv`
 5. Further tests were written to verify the consistency of the data.
 6. Finally fixed values like `country`, `language`, and `genre` was extracted and SQL insert scripts were created for these.
 7. For remaining tables, another script `data/jumbo_load.py` was written to  run over the CSVs and insert everything into the database directly.

## What technologies does it use?
 1. PostgreSQL
 2. Django
 3. psycopg2
 4. HTML
 5. JavaScript
 6. charts.js
 7. d3.js
 8. venn.js
 9. Bootflat
 10. CSS

## How to set it up?
1. `git clone https://github.tamu.edu/sswt/justmovies.git`
2. `cd path/to/project`
3. create `virtualenv` if you want. Recommended!!
4. Install requirements with `pip install -r requirements.txt`
5. Now create a fresh database in postgres.
6. Add its credentials to `utils/credentials.py`
7. Run `data/data_load.py`. This will take around 2 minutes to complete. If everything goes well, you will have the complete database after it ends.
8. Alternatively, you can load data into postgres directly using the `data/dump.sql` pg_dump.
9. Migrate `python manage.py migrate`. Although the application logic uses postgres, Django uses sqlite here. I did not change this because in a course project, I want to keep these separate.
10. Start up the server `python manage.py runserver`

## Screenshots
![Movies Listing](https://i.imgur.com/oH94zgo.png)
![Individual Celebrity Page](https://i.imgur.com/y0Tq5Yq.png)
![Data Page](https://i.imgur.com/xTF76jy.png)
![Edit Movie Page](https://i.imgur.com/jpQjzjI.png)

## How to reach me if there's some issue?
If you have access, create an issue in this repo.
Otherwise send me an email at sswt at tamu dot edu.