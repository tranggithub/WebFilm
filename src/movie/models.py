from distutils.command.upload import upload
from email.mime import image
from pydoc import describe
from statistics import mode
from django.db import models
# from multiselectfield import Multiselectfield

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.
CATEGORY_CHOICE = (
    ('Action','ACTION'),
    ('Drama','DRAMA'),
    ('Comedy','COMEDY'),
    ('Romance','ROMANCE'),
    ('Adventure', 'ADVENTURE'),
    ('Documentary','DOCUMENTARY'),
    ('Family','FAMILY'),
    ('Historical','HISTORICAL'),
    ('Musical','MUSICAL'),
    ('Horror','HORROR'),
    ('Science fiction','SCIENCE FICTION'),
    ('Tragedy','TRAGEDY'),
    ('War','WAR'),
    ('Westerns','WESTERNS'),
)

LAGUAGE_CHOICES = (
    ('EN','ENGLISH'),
    ('VI','VIETNAM'),
)

STATUS_CHOICES = (
    ('RA','RECENTLY ADDED'),
    ('MW','MOST WATCHED'),
    ('TR', 'TOP RATED'),
    ('T', 'TRENDING'),
    ('U', 'UPCOMING'),
)
GENDER_CHOICES = (
    ('F','FEMALE'),
    ('M','MALE'),
    ('O', 'OTHERS'),
    ('N', 'NO INFORMATION'),
)
FORMAT_CHOICES = (
    ('TV', 'TV SERIES'),
    ('PS', 'POPULAR MOVIES ON SEPTEMBER'),
    ('F', 'FEATURE')
)
NATIONAL_CHOICES = (
    ('Argentina','ARGENTINA'),
    ('Australia','AUSTRALIA'),
    ('Belgium','BELGIUM'),
    ('Brazil','BRAZIL'),
    ('Canada','CANADA'),
    ('China','CHINA'),
    ('USA', 'USA'),
    ('Vietnamese', 'VIETNAMESE')
)

# class CAST_CREW (models.Model):
#     name = models.CharField(max_length=255)
#     movie = models.ManyToManyField('Movie', related_name='movie_cast')

class Cast_and_Crew(models.Model):
    # name_actor_crew = models.ForeignKey(CAST_CREW, on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    title_movie = models.CharField(max_length=255)
    character = models.CharField(max_length=255)
    sub_character = models.CharField(max_length=255, blank=True, null=True) #not required
    image = models.ImageField(upload_to='cast', default="/cast/noimage.jpg")
    
    def __str__(self):
        return str(self.name) + ' - ' + self.character

    class Meta:
        verbose_name = 'Cast and Crew'
        verbose_name_plural='Casts and Crews'

class Category(models.Model):
    movie = models.ManyToManyField('Movie', related_name='movie_category')
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=15, unique=True)

    def __str__(self):
        return str(self.category)
    class Meta:
        verbose_name_plural = 'Categories'

class Statuses(models.Model):
    status = models.CharField(choices=STATUS_CHOICES, max_length=2, unique=True)

    def __str__(self):
        return str(self.status)
    
    class Meta:
        verbose_name_plural = 'Statuses'

class Movie(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='movies')
    trailer = models.FileField(upload_to='trailers', null=True)
    trailer_image = models.ImageField(upload_to='trailer_image', null=True)
    national = models.CharField(choices=NATIONAL_CHOICES,max_length=10)
    status = models.ManyToManyField(Statuses, verbose_name='status')
    language = models.CharField(choices=LAGUAGE_CHOICES,max_length=2)
    year_of_production = models.DateField()
    views_count = models.IntegerField(default=0)
    time = models.CharField(default='2h10m', max_length=6)
    director = models.CharField(max_length=100)
    writers = models.CharField(max_length=255)
    
    #stars
    cast_and_crew = models.ManyToManyField(Cast_and_Crew, related_name='cast_crew')
    format = models.CharField(choices=FORMAT_CHOICES, max_length=2)
    trivia_summary = models.CharField(max_length=500)
    trivia_image = models.ImageField(upload_to='trivia', null=True)
    trivia_url = models.URLField(max_length=500, null=True)

    def __str__(self):
        return str(self.title) 

class Episode(models.Model):
    title = models.ForeignKey(Movie,related_name="movie_episode", on_delete=models.CASCADE)
    # episodes = models.AutoField()
    number_episode = models.IntegerField(default=1)
    video = models.FileField(upload_to='episodes', null=True)
    
    def __str__(self):
        return str(self.number_episode)    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='user_profile',null=True, default='user_profile/anonymous.PNG')
    birthday = models.DateField(null=True, blank=True, default='2022-01-01')
    gender = models.CharField(choices=GENDER_CHOICES,max_length=1,default='N')

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    movie = models.ForeignKey(Movie,related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, related_name="publisher", on_delete=models.CASCADE)
    #avatar = models.ImageField(default='user_profile/anonymous.PNG')
    #name = models.CharField(max_length=255, null=True,blank=True, default=user.)
    body = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        # self.avatar = self.user.avatar
        # self.name = self.user.user.first_name
        return '%s - %s' % (self.movie.title,self.user.user.first_name)
# Tin hieu thong bao them user moi -> Them Profile moi
@receiver(post_save, sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)