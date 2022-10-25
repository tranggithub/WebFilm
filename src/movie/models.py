from distutils.command.upload import upload
from email.mime import image
from pydoc import describe
from statistics import mode
from django.db import models

# Create your models here.
CATEGORY_CHOICE = (
    ('A','ACTION'),
    ('D','DRAMA'),
    ('C','COMEDY'),
    ('R','ROMANCE'),

)

LAGUAGE_CHOICES = (
    ('EN','ENDLISH'),
    ('VI','VIETNAM'),
)

STATUS_CHOICES = (
    ('RA','RECENTLY ADDED'),
    ('MW','MOST WATCHED'),
    ('TR', 'TOP RATED'),
)
class Movie(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='movies')
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=1)
    language = models.CharField(choices=LAGUAGE_CHOICES,max_length=2)
    status = models.CharField(choices=STATUS_CHOICES,max_length=2)
    year_of_production = models.DateField()
    views_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.title) 