from ast import Mod
from django.http import HttpResponse
from pyexpat import model
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django import forms
# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Movie, Profile

class MovieList (ListView):
    model = Movie
    
class MovieDetailView (DetailView):
    model = Movie

def SignUp(request):
  if request.method == "POST":
    usernm = request.POST.get('username')
    mail = request.POST.get('email')
    passwd1 = request.POST.get('password1')
    passwd2 = request.POST.get('password2')
    if passwd1 == passwd2:
      try:
        user= User.objects.get(username=usernm)
        messages.error(request,"The username you entered has already been taken. Please try another username.")
        return redirect('/movies/sign_up')
      except User.DoesNotExist:
        nm = request.POST.get('name')
        myuser = User.objects.create_user(username=usernm,email=mail,password=passwd1)
        myuser.first_name = nm
        myuser.save()
        messages.success(request,"Your account has been created successfully")
        return redirect('/movies/log_in')
    else:
      messages.error(request,"Your confirm password and your password are not the same")
      return redirect('/movies/sign_up')
  return render(request,".\SignUp_LogIn\SignUpFilm.html")


def LogIn(request):
  if request.user.is_authenticated:
    messages.warning(request, "You have already logged in")
    return redirect('/movies/userpacket')
  else:
    if request.method == "POST":
      name = request.POST.get('username')
      passwd = request.POST.get('password')
      user = authenticate(request,username=name,password=passwd)
      if user is not None:
        login(request, user)
        messages.success(request,"Log in successfully")
        return redirect('/movies/userpacket')
      else:
        messages.error(request,"Invalid Username or Password")
        return redirect('/movies/log_in')
    return render(request,".\SignUp_LogIn\LogInFilm.html")

@login_required
def Home(request):
  ava = request.user.profile.avatar.url
  movies = Movie.objects.all()
  trending = Movie.objects.filter(status__status='T')[:4]
  upcoming = Movie.objects.filter(status__status='U')[:4]
  tv_series = Movie.objects.filter(format='TV')[:4]
  ps = Movie.objects.filter(format='PS')[:4]
  return render(request,"Home/Home.html",{'avatar':ava, 'movies': movies,'trending': trending, 'upcoming':upcoming, 'tv_series':tv_series, 'ps':ps})


def SeeAll_Trending(request):
  ava = request.user.profile.avatar.url
  movies = Movie.objects.filter(status__status='T')
  return render(request,".\Home\SeeAll_Trending_English.html",{'avatar':ava, 'movies':movies})


def Loading_Circle(request):
  template = loader.get_template('.\Loading_Screen_Logo\loading_screen.html')
  return HttpResponse(template.render())

def Loading_Logo(request):
  template = loader.get_template('.\Loading_Screen_Logo\sign_up.html')
  return HttpResponse(template.render())

def LogOut(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Log out successfully")
    return redirect('/movies/log_in')

def Movies(request):
  ava = request.user.profile.avatar.url
  movies = Movie.objects.all()[:4]
  upcoming = Movie.objects.filter(status__status='U')[:4]
  tv_series = Movie.objects.filter(format='TV')[:4]
  ps = Movie.objects.filter(format='PS')[:4]
  return render(request,"Movies/movies.html",{'avatar':ava, 'movies': movies, 'upcoming':upcoming, 'tv_series':tv_series, 'ps':ps})

def WatchFilm(request, movie_id):
  ava = request.user.profile.avatar.url
  movies = Movie.objects.filter(id=movie_id)
  episode = movies.get().movie_episode.all()
  return render(request,".\Trailer_Detail\Watch.html",{'avatar':ava, 'movies': movies, 'episode': episode})

def Detail(request, movie_id):
  ava = request.user.profile.avatar.url
  another = Movie.objects.all().exclude(id=movie_id)[:4]
  movies = Movie.objects.filter(id=movie_id)
  category = movies.get().movie_category.all()
  cast_crew = movies.get().cast_and_crew.all()
  topcast = cast_crew[:4]
  return render(request,".\Trailer_Detail\Trailer_Detail.html",{'avatar':ava, 'another': another, 'movies': movies, 'category': category, 'topcast': topcast, 'cast_crew': cast_crew})


def UserPacket(request):
  template = loader.get_template('UserPacket\Service_pack.html')
  return HttpResponse(template.render())

class UserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ("first_name","email")

class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ("avatar","birthday","gender")

def Info(request):
  nm = request.user.first_name
  mail = request.user.email
  sex = request.user.profile.get_gender_display
  ava = request.user.profile.avatar.url
  bd = request.user.profile.birthday
  return render(request,".\Info\info.html",{'name':nm, 'email':mail, 'gender':sex,'avatar':ava,'birthday':bd})

#Đồng nhất khi thay đổi dữ liệu
@transaction.atomic
def ChangeInfo(request):
  if request.method == "POST":
    user_form = UserForm(request.POST, instance=request.user)
    user_profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
    if user_form.is_valid() and user_profile_form.is_valid():
      user_form.save()
      user_profile_form.save()
      messages.success(request,"Change information of your account successfully")
      return redirect('/movies/info')
    else:
      messages.error(request,"Invalid value")
  else:
    user_form = UserForm(instance=request.user)
    user_profile_form = ProfileForm(instance=request.user.profile)
  return render(request,'.\Info\change_info.html',{'u_form':user_form, 'p_form':user_profile_form}) 
  # template = loader.get_template('.\Info\change_date.html')
  # return HttpResponse(template.render())


# def ChangePassword(request):
#   template = loader.get_template('.\Info\change_password.html')
#   return HttpResponse(template.render())
