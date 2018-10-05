from django.views import View
from django.shortcuts import render

from utils.db_utils import DatabaseUtils

class HomeView(View):
    def get(self, request):
        db = DatabaseUtils()
        query = """SELECT * FROM movie LIMIT 10;"""
        db.get_cursor().execute(query);
        all_movies = db.get_cursor().fetchall()
        context = {
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
            } for m in all_movies]
        }
        print(context["movies"][0])
        return render(request, 'justmovies/index.html', context)