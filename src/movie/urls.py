
from django.urls import path, include
from .views import MovieList, MovieDetailView, MovieNational, SeeAll_Trending_Filer,MovieCategory,MovieFormat,MovieSort,MovieCondition,MovieYear
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    #test
    path('', MovieList.as_view(), name='movie_list'),
    path('<int:pk>', MovieDetailView.as_view(), name='movie_detail'),
    path("accounts/", include("django.contrib.auth.urls")),


    # Add url filter in see all
    path('national/<str:Nation>',MovieNational.as_view(),name='national'),
    path('SeeAll_Filter/',views.SeeAll_Trending_Filer.as_view(),name='SeeAll_Filter'),
    path('category/<str:cate>',MovieCategory.as_view(),name='category'),
    path('format/<str:for>',MovieFormat.as_view(),name='format'),
    path('sort/<str:so>',MovieSort.as_view(),name='sort'),
    path('condition/<str:condi>',MovieCondition.as_view(),name='condition'),
    path('year/<int:year>',MovieYear.as_view(),name='movie_year'),
    


    path('home/',views.Home, name='home'),
    path('loading_circle/',views.Loading_Circle,name='loading_circle'),
    path('loading_logo/',views.Loading_Logo,name='loading_logo'),
    path('log_in/',views.LogIn, name='log_in'),
    path('log_out/',views.LogOut, name='log_out'),
    path('sign_up/',views.SignUp, name='sign_up'),
    path('movies/',views.Movies, name='movies'),
    path('library/',views.Library, name='library'),
    path('watch/<movie_id>/<number_ep>',views.WatchFilm, name='watch'),
    path('detail/<movie_id>',views.Detail, name='detail'),
    path('userpacket/',views.UserPacket, name='userpacket'),
    path('seeall_trending_english/<status_short>', views.SeeAll_Trending, name='seeall_trending_english'),
    path('info/',views.Info,name='info'),
    path('change_info/',views.ChangeInfo,name='change_info'),
    path('change_password/',auth_views.PasswordChangeView.as_view(
        template_name='./Info/change_password.html',
        success_url = '/movies/info'
    ),name='change_password'),

    path("reset_password/", views.password_reset_request, name="reset_password"),
    # path('reset_password/',auth_views.PasswordResetView.as_view(
    #     template_name='./Info//reset_password.html',
    #     success_url = '/movies/log_in'
    # ),name='reset_password'),
    path('reset_password/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(
        template_name='./Info//reset_confirm.html',
        success_url = '/movies/reset_password/complete'
    ),name='reset_confirm'),
    path('reset_password/done',auth_views.PasswordResetDoneView.as_view(
        template_name='./Info//reset_done.html',
    ),name='reset_done'),
    path('reset_password/complete',auth_views.PasswordResetCompleteView.as_view(
        template_name='./Info//reset_complete.html',
    ),name='reset_complete'),
    path('search/',views.searchBar, name='search'),
 
]

