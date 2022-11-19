from django.contrib import admin

# Register your models here.
from .models import Movie
from .models import Cast_and_Crew


admin.site.register(Movie)
admin.site.register(Cast_and_Crew)