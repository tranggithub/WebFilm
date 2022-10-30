
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
    path('userpacket/',views.UserPacket, name='userpacket'),
    path('seeall_trending_english/', views.SeeAll_Trending, name='seeall_trending_english'),
    path('info/',views.Info,name='info'),
    path('change_bdate/',views.ChangeBDate,name='change_bdate'),
    path('change_gender/',views.ChangeGender,name='change_gender'),
    path('change_mail/', views.ChangeMail,name='change_mail'),
    path('change_name/',views.ChangeName,name='change_name'),
    path('change_password/',views.ChangePassword,name='change_password'),
    path('change_picture/',views.ChangePicture,name='change_picture'),
]
