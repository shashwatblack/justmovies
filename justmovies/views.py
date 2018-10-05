from django.http import HttpResponse
from django.views import View

from utils.db_utils import DatabaseUtils

class HomeView(View):
    def get(self, request):
        db = DatabaseUtils()
        query = """SELECT * FROM country;"""
        db.get_cursor().execute(query);
        return HttpResponse(
            db.get_cursor().fetchall()
        )