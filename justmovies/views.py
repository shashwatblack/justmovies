from django.views import View
from django.shortcuts import render

from utils.db_utils import DatabaseUtils


class HomeView(View):
    def get(self, request):
        db = DatabaseUtils()

        filters = {
            "title": request.GET.get('title', ''),
            "company": request.GET.get('company', ''),
            "year_gte": request.GET.get('year_gte', ''),
            "year_lte": request.GET.get('year_lte', '')
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
            "pagination": pagination
        }
        return render(request, 'justmovies/index.html', context)