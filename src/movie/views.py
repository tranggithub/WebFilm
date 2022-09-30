from ast import Mod
from pyexpat import model
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Movie

class MovieList (ListView):
    model = Movie
    
class MovieDetailView (DetailView):
    model = Movie