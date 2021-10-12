from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.

from .models import Movie

class MoviesView(View):
    """
    Список фильмов
    """
    def get(self, request):
        movies = Movie.objects.all()
        return render(request, "movie/movie_list.html", {'movie_list': movies})



