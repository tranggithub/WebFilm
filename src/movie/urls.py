
from django.urls import path
from .views import MovieList, MovieDetailView

urlpatterns = [
    path('', MovieList.as_view(), name='movie_list'),
    path('<int:pk>', MovieDetailView.as_view(), name='movie_detail'),
]
