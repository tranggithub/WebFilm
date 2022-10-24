
from django.urls import path
from .views import MovieList, MovieDetailView
from . import views
urlpatterns = [
    path('', MovieList.as_view(), name='movie_list'),
    path('<int:pk>', MovieDetailView.as_view(), name='movie_detail'),
    path('home/',views.Home, name='home'),
    path('loading_circle/',views.Loading_Circle,name='loading_circle'),
    path('loading_logo/',views.Loading_Logo,name='loading_logo'),
    path('log_in/',views.LogIn, name='log_in'),
    path('sign_up/',views.SignUp, name='sign_up'),
    path('movies/',views.Movies, name='movies'),
    path('watch/',views.WatchFilm, name='watch'),
    path('detail/',views.Detail, name='detail'),
]
