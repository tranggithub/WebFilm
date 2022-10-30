from ast import Mod
from django.http import HttpResponse
from pyexpat import model
from django.template import loader
from django.shortcuts import render

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
  template = loader.get_template('.\SignUp_LogIn\LogInFilm.html')
  return HttpResponse(template.render())

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