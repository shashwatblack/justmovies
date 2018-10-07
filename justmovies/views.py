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
            if abs(movies["pagination"]["page_number"] - i) <= 2
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


class PeopleView(View):
    def get(self, request):
        db = DatabaseUtils()
        name = request.GET.get('name', '')

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