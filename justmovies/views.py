from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render

from utils.db_utils import DatabaseUtils
from utils.enums import Enums


class MoviesView(View):
    def get(self, request):
        db = DatabaseUtils()

        filters = {
            "title": request.GET.get('title', ''),
            "company": request.GET.get('company', ''),
            "year_gte": request.GET.get('year_gte', ''),
            "year_lte": request.GET.get('year_lte', ''),
            "imdb_rating": request.GET.get('imdb_rating', '')
        }

        movies = db.get_movies(filters, page_number=int(request.GET.get('page', '1')))

        pagination = {
            "page_number": movies["pagination"]["page_number"],
            "page_size": movies["pagination"]["page_size"],
            "total_hits": movies["pagination"]["total_hits"],
            "total_pages": movies["pagination"]["total_pages"],
            "pages": None
        }

        pages = [
            i for i in range(1, movies["pagination"]["total_pages"] + 1)
            if abs(movies["pagination"]["page_number"] - i) <= 4
        ]

        if len(pages):
            if pages[0] != 1:
                pages = ['...'] + pages

            if pages[-1] != movies["pagination"]["total_pages"]:
                pages = pages + ['...']

        pagination["pages"] = pages

        context = {
            "filters": filters,
            "movies": [{
                "pk": m[0],
                "title": m[1],
                "year": m[2],
                "company": m[3],
                "budget": m[4],
                "gross": m[5],
                "released": m[6],
                "runtime": m[7],
                "plot": m[8],
                "awards": m[9],
                "poster": m[10],
                "website": m[11],
                "imdb_rating": m[12],
                "imdb_id": m[13],
                "country": m[14],
                "rating": m[15],
                "genre": m[16],
                "language": m[17]
            } for m in movies["values"]],
            "pagination": pagination,
            "ratings": Enums.imdb_ratings
        }
        return render(request, 'justmovies/index.html', context)


class MovieEditView(View):
    def get_context_data(self, movie_pk):
        db = DatabaseUtils()
        movie = db.get_movie_from_pk(movie_pk)
        context = {
            "movie": {
                "pk": movie[0],
                "title": movie[1],
                "year": movie[2],
                "company": movie[3],
                "budget": movie[4],
                "gross": movie[5],
                "released": movie[6],
                "runtime": movie[7],
                "plot": movie[8],
                "awards": movie[9],
                "poster": movie[10],
                "website": movie[11],
                "imdb_rating": movie[12],
                "imdb_id": movie[13],
                "country": movie[14],
                "rating": movie[15],
                "genre": movie[16],
                "language": movie[17]
            },
            "countries": [{
                "pk": c[0],
                "name": c[1]
            } for c in db.countries],
            "ratings": [{
                "pk": c[0],
                "name": c[1]
            } for c in db.mpaa_ratings],
            "genres": [{
                "pk": c[0],
                "name": c[1]
            } for c in db.genres],
            "languages": [{
                "pk": c[0],
                "name": c[1]
            } for c in db.languages]
        }
        return context

    def get(self, request, movie_pk):
        return render(request, 'justmovies/movie_edit.html', self.get_context_data(movie_pk))

    def post(self, request, movie_pk):
        db = DatabaseUtils()
        if request.POST.get("action", "update") == "delete":
            db.delete_movie(movie_pk)
            return HttpResponseRedirect('/')

        db.update_movie(movie_pk, {
            "title": request.POST.get("title", ""),
            "year": request.POST.get("year", ""),
            "company": request.POST.get("company", ""),
            "budget": request.POST.get("budget", ""),
            "gross": request.POST.get("gross", ""),
            "released": request.POST.get("released", ""),
            "runtime": request.POST.get("runtime", ""),
            "plot": request.POST.get("plot", ""),
            "awards": request.POST.get("awards", ""),
            "poster": request.POST.get("poster", ""),
            "website": request.POST.get("website", ""),
            "imdb_rating": request.POST.get("imdb_rating", ""),
            "imdb_id": request.POST.get("imdb_id", ""),
            "country": request.POST.get("country", ""),
            "rating": request.POST.get("rating", ""),
            "genre": request.POST.get("genre", ""),
            "language": request.POST.get("language", "")
        })
        return render(request, 'justmovies/movie_edit.html', self.get_context_data(movie_pk))


class PeopleView(View):
    def get(self, request):
        db = DatabaseUtils()
        name = request.GET.get('name', 'Stephen King')

        if not name:
            return render(request, 'justmovies/people.html', {"success": False})

        person = db.get_people(name)

        if not person:
            return render(request, 'justmovies/people.html', {"success": False, "name": name})

        person = person[0]

        roles = db.get_personal_roles(person)
        roles = ', '.join([r[1] for r in roles])

        involvements = db.get_involvements(person)
        involvements = [{
            "movie_pk": i[0],
            "title": i[1],
            "year": i[2],
            "awards": i[9],
            "poster": i[10],
            "role": i[18]
        } for i in involvements]

        context = {
            "success": True,
            "name": person[1],
            "dob": person[2],
            "image": person[3],
            "intro": person[4],
            "roles": roles,
            "involvements": involvements,
        }
        return render(request, 'justmovies/people.html', context)


class DataView(View):
    def get(self, request):
        db = DatabaseUtils()
        cursor = db.get_cursor()

        cursor.execute("SELECT COUNT(*), MIN(year), MAX(year), SUM(budget) FROM movie;")
        moviesGeneral = cursor.fetchone()

        cursor.execute("SELECT COUNT(*) FROM person;")
        peopleGeneral = cursor.fetchone()

        general = {
            "moviesCount": moviesGeneral[0],
            "moviesMinYear": moviesGeneral[1],
            "moviesMaxYear": moviesGeneral[2],
            "moviesBudget": moviesGeneral[3] // 1000000,
            "totalPeople": peopleGeneral[0],
            "totalReviews": 0,
        }

        # DISTRIBUTION BY GENRE
        cursor.execute("select g.name, count(*) from movie m join genre g on m.genre = g.pk group by g.name order by -count(*) limit 8;")
        countDistByGenre = cursor.fetchall()
        cursor.execute("select count(*) from movie m join genre g on m.genre = g.pk group by g.name order by -count(*) offset 8;")
        remainingGenres = cursor.fetchall()
        remainingGenres = sum([r[0] for r in remainingGenres])
        countDistByGenre = {
            "datasets": [{
                "data": [g[1] for g in countDistByGenre] + [remainingGenres],
                "backgroundColor": Enums.colors[:len(countDistByGenre)] + [Enums.colors_others]
            }],
            "labels": [g[0] for g in countDistByGenre] + ["Others"]
        }

        # DISTRIBUTION BY COUNTRY
        cursor.execute("select c.name, count(*) from movie m join country c on m.country = c.pk group by c.name order by -count(*) limit 5;")
        countDistByCountry = cursor.fetchall()
        cursor.execute("select count(*) from movie m join country c on m.country = c.pk group by c.name order by -count(*) offset 5;")
        remainingCountries = cursor.fetchall()
        remainingCountries = sum([r[0] for r in remainingCountries])
        countDistByCountry = {
            "datasets": [{
                "data": [g[1] for g in countDistByCountry] + [remainingCountries],
                "backgroundColor": Enums.colors[:len(countDistByCountry)] + [Enums.colors_others]
            }],
            "labels": [g[0] for g in countDistByCountry] + ["Others"]
        }

        # DISTRIBUTION BY LANGUAGE
        cursor.execute("select c.name, count(*) from movie m join language c on m.language = c.pk group by c.name order by -count(*) limit 5;")
        countDistByLanguage = cursor.fetchall()
        cursor.execute("select count(*) from movie m join language c on m.language = c.pk group by c.name order by -count(*) offset 5;")
        remainingLanguages = cursor.fetchall()
        remainingLanguages = sum([r[0] for r in remainingLanguages])
        countDistByLanguage = {
            "datasets": [{
                "data": [g[1] for g in countDistByLanguage] + [remainingLanguages],
                "backgroundColor": Enums.colors[:len(countDistByLanguage)] + [Enums.colors_others]
            }],
            "labels": [g[0] for g in countDistByLanguage] + ["Others"]
        }

        # BUDGET DISTRIBUTION BY GENRE
        cursor.execute("select g.name, sum(budget) from movie m join genre g on m.genre = g.pk group by g.name order by -count(*) limit 8;")
        budgetDistByGenre = cursor.fetchall()
        cursor.execute("select sum(budget) from movie m join genre g on m.genre = g.pk group by g.name order by -count(*) offset 8;")
        remainingGenres = cursor.fetchall()
        remainingGenres = sum([r[0] for r in remainingGenres])
        budgetDistByGenre = {
            "datasets": [{
                "data": [g[1] for g in budgetDistByGenre] + [remainingGenres],
                "backgroundColor": Enums.colors[:len(budgetDistByGenre)] + [Enums.colors_others]
            }],
            "labels": [g[0] for g in budgetDistByGenre] + ["Others"]
        }

        # BUDGET DISTRIBUTION BY COUNTRY
        cursor.execute("select c.name, sum(budget) from movie m join country c on m.country = c.pk group by c.name order by -count(*) limit 5;")
        budgetDistByCountry = cursor.fetchall()
        cursor.execute("select sum(budget) from movie m join country c on m.country = c.pk group by c.name order by -count(*) offset 5;")
        remainingCountries = cursor.fetchall()
        remainingCountries = sum([r[0] for r in remainingCountries])
        budgetDistByCountry = {
            "datasets": [{
                "data": [g[1] for g in budgetDistByCountry] + [remainingCountries],
                "backgroundColor": Enums.colors[:len(budgetDistByCountry)] + [Enums.colors_others]
            }],
            "labels": [g[0] for g in budgetDistByCountry] + ["Others"]
        }

        # BUDGET DISTRIBUTION BY LANGUAGE
        cursor.execute("select c.name, sum(budget) from movie m join language c on m.language = c.pk group by c.name order by -count(*) limit 5;")
        budgetDistByLanguage = cursor.fetchall()
        cursor.execute("select sum(budget) from movie m join language c on m.language = c.pk group by c.name order by -count(*) offset 5;")
        remainingLanguages = cursor.fetchall()
        remainingLanguages = sum([r[0] for r in remainingLanguages])
        budgetDistByLanguage = {
            "datasets": [{
                "data": [g[1] for g in budgetDistByLanguage] + [remainingLanguages],
                "backgroundColor": Enums.colors[:len(budgetDistByLanguage)] + [Enums.colors_others]
            }],
            "labels": [g[0] for g in budgetDistByLanguage] + ["Others"]
        }

        # BUDGET DISTRIBUTION BY YEAR
        cursor.execute("select year, sum(budget) from movie group by year order by year;")
        budgetDistByYear = cursor.fetchall()
        budgetDistByYear = {
            "datasets": [{
                "data": [g[1] for g in budgetDistByYear],
                "backgroundColor": Enums.colors[:len(budgetDistByYear)]
            }],
            "labels": [g[0] for g in budgetDistByYear]
        }

        # ROLES DISTRIBUTION
        cursor.execute("SELECT count(person.pk), role FROM person JOIN personal_role ON person.pk = personal_role.person group by personal_role.role;")
        celebrityRoleDistribution = cursor.fetchall()
        celebrityRoleDistribution = [{
            "sets": [c[1]],
            "size": c[0]
        } for c in celebrityRoleDistribution]
        cursor.execute("select count(*) from person where "
                       "person.pk in (select person from involvement where role='Writer') and "
                       "person.pk in (select person from involvement where role='Actor');")
        result = cursor.fetchone()
        celebrityRoleDistribution.append({
            "sets": ["Writer", "Actor"],
            "size": result[0]
        })
        cursor.execute("select count(*) from person where "
                       "person.pk in (select person from involvement where role='Director') and "
                       "person.pk in (select person from involvement where role='Actor');")
        result = cursor.fetchone()
        celebrityRoleDistribution.append({
            "sets": ["Director", "Actor"],
            "size": result[0]
        })
        cursor.execute("select count(*) from person where "
                       "person.pk in (select person from involvement where role='Writer') and "
                       "person.pk in (select person from involvement where role='Director');")
        result = cursor.fetchone()
        celebrityRoleDistribution.append({
            "sets": ["Writer", "Director"],
            "size": result[0]
        })
        cursor.execute("select count(*) from person where "
                       "person.pk in (select person from involvement where role='Writer') and "
                       "person.pk in (select person from involvement where role='Director') and "
                       "person.pk in (select person from involvement where role='Actor');")
        result = cursor.fetchone()
        celebrityRoleDistribution.append({
            "sets": ["Writer", "Actor", "Director"],
            "size": result[0]
        })

        # TOP RATED CELEBRITIES
        cursor.execute("""
            select
              ip.name,
              avg(NULLIF(imdb_rating, 'N/A') :: float) as avg_rating,
              count(*)                                 as movie_count
            from movie m
              join (select
                      p.name,
                      i.movie
                    from person p
                      join involvement i on p.pk = i.person) ip on ip.movie = m.pk
            group by ip.name
            having count(*) >= 10
            order by -avg(NULLIF(imdb_rating, 'N/A') :: float)
            limit 10;
        """)
        topRatedCelebrities = cursor.fetchall()
        topRatedCelebrities = [{
            "name": t[0],
            "avg_rating": '{0:.2f}'.format(t[1]),
            "movie_count": t[2]
        } for t in topRatedCelebrities]

        context = {
            "general": general,
            "countDistByGenre": countDistByGenre,
            "countDistByCountry": countDistByCountry,
            "countDistByLanguage": countDistByLanguage,
            "budgetDistByGenre": budgetDistByGenre,
            "budgetDistByCountry": budgetDistByCountry,
            "budgetDistByLanguage": budgetDistByLanguage,
            "budgetDistByYear": budgetDistByYear,
            "celebrityRoleDistribution": celebrityRoleDistribution,
            "topRatedCelebrities": topRatedCelebrities
        }
        return render(request, 'justmovies/data.html', context)