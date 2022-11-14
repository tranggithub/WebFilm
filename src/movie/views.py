from ast import Mod
from django.http import HttpResponse
from pyexpat import model
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Movie

class MovieList (ListView):
    model = Movie
    
class MovieDetailView (DetailView):
    model = Movie

def Home(request):
  template = loader.get_template('.\Home\Home.html')
  return HttpResponse(template.render())

def SeeAll_Trending(request):
  template = loader.get_template('.\Home\SeeAll_Trending_English.html')
  return HttpResponse(template.render())

def Loading_Circle(request):
  template = loader.get_template('.\Loading_Screen_Logo\loading_screen.html')
  return HttpResponse(template.render())

def Loading_Logo(request):
  template = loader.get_template('.\Loading_Screen_Logo\sign_up.html')
  return HttpResponse(template.render())

def SignUp(request):
  template = loader.get_template('.\SignUp_LogIn\SignUpFilm.html')
  return HttpResponse(template.render())

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
        messages.success(request,"Login successfully")
        return redirect('/movies/userpacket')
      else:
        messages.error(request,"Invalid Username or Password")
        return redirect('/movies/log_in')
    return render(request,".\SignUp_LogIn\LogInFilm.html")

# def LogIn(request):
#   template = loader.get_template('.\SignUp_LogIn\LogInFilm.html')
#   return HttpResponse(template.render())

def Movies(request):
  template = loader.get_template('.\Movies\movies.html')
  return HttpResponse(template.render())

def WatchFilm(request):
  template = loader.get_template('.\Trailer_Detail\Watch.html')
  return HttpResponse(template.render())

def Detail(request):
  template = loader.get_template('.\Trailer_Detail\Trailer_Detail.html')
  return HttpResponse(template.render())

def UserPacket(request):
  template = loader.get_template('UserPacket\Service_pack.html')
  return HttpResponse(template.render())

def Info(request):
  template = loader.get_template('.\Info\info.html')
  return HttpResponse(template.render())

def ChangeBDate(request):
  template = loader.get_template('.\Info\change_date.html')
  return HttpResponse(template.render())

def ChangeGender(request):
  template = loader.get_template('.\Info\change_gender.html')
  return HttpResponse(template.render())

def ChangeMail(request):
  template = loader.get_template('.\Info\change_mail.html')
  return HttpResponse(template.render())

def ChangeName(request):
  template = loader.get_template('.\Info\change_name.html')
  return HttpResponse(template.render())

def ChangePassword(request):
  template = loader.get_template('.\Info\change_password.html')
  return HttpResponse(template.render())

def ChangePicture(request):
  template = loader.get_template('.\Info\change_picture.html')
  return HttpResponse(template.render())