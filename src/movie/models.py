from distutils.command.upload import upload
from email.mime import image
from pydoc import describe
from statistics import mode
from django.db import models
# from multiselectfield import Multiselectfield

from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
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
    trailer_video = models.URLField(max_length=1000, null=True)
    # trailer_image = models.ImageField(upload_to='trailer_image', null=True)
    national = models.CharField(choices=NATIONAL_CHOICES,max_length=10)
    status = models.ManyToManyField(Statuses, verbose_name='status')
    categories = models.ManyToManyField(Category, verbose_name='category')
    language = models.CharField(choices=LAGUAGE_CHOICES,max_length=2)
    year_of_production = models.DateField()
    views_count = models.IntegerField(default=0)
    time = models.CharField(default='2h10m', max_length=6)
    
    #Love and mark video
    loves = models.ManyToManyField(User,related_name="movie_love", verbose_name="loves", null=True, blank=True)
    marks = models.ManyToManyField(User,related_name="movie_mark", null=True, blank=True)
    history = models.ManyToManyField(User,related_name="movie_history", null=True, blank=True)

    #Hỗ trợ chức năng đổi icon 
    who_has_it_open = models.IntegerField(null=True,blank=True,default=0)

    director = models.CharField(max_length=100)
    writers = models.CharField(max_length=255)
    cast_and_crew = models.ManyToManyField(Cast_and_Crew, related_name='cast_crew')
    format = models.CharField(choices=FORMAT_CHOICES, max_length=2)
    trivia_summary = models.CharField(max_length=500)
    trivia_image = models.ImageField(upload_to='trivia', null=True)
    trivia_url = models.URLField(max_length=500, null=True)

    def __str__(self):
        return str(self.title) 

    # Xem người dùng hiện tại đã đánh dấu chưa
    def is_love(self):
        return self.loves.filter(id=self.who_has_it_open).exists()
    def is_mark(self):
        return self.marks.filter(id=self.who_has_it_open).exists()

    #Tính trung bình đánh giá sao
    def average_of_star(self):
        myrate = RatingStar.objects.all()
        myrate = myrate.filter(movie__id=self.id)
        sum = 0
        for i in myrate:
            sum = sum + i.rate
        if myrate.count() == 0:
            return 0
        return sum/(myrate.count())
    def only_parent_comment(self):
        return Comment.objects.filter(movie=self,parent=None)
    
    def total_views(self):
        return self.history.count()
    
    #Query gernes
    def query_gernes(self):
        gernes = ""
        for i in self.categories.all():
            gernes = gernes + '|' + i.category
        return gernes
    
class Episode(models.Model):
    title = models.ForeignKey(Movie,related_name="movie_episode", on_delete=models.CASCADE)
    number_episode = models.IntegerField(default=1)
    episode = models.URLField(max_length=1000, null=True)
    
    def __str__(self):
        return str(self.number_episode)    

class Award(models.Model):
    movie = models.ForeignKey(Movie ,related_name="movie_award", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True, default=' ')
    def __str__(self):
        return '%s - %s' % (self.movie.title, self.name)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='user_profile',null=True, default='user_profile/anonymous.PNG')
    birthday = models.DateField(null=True, blank=True, default='2022-01-01')
    gender = models.CharField(choices=GENDER_CHOICES,max_length=1,default='N')

    #Hỗ trợ việc cần thông báo đến người dùng có film mới hay không
    is_need_to_notify = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    def send_notification(self, title, description):
        if self.is_need_to_notify:
            subject = "A New Movie Notification"
            email_template_name = "./Info/notification.txt"
            c = {
            "email":self.user.email,
            'domain':'127.0.0.1:8000',
            'site_name': 'LTWFlix',
            "user": self.user,
            'protocol': 'http',
            "title": title,
            "description":description
            }
            email = render_to_string(email_template_name, c)
            try:
                send_mail(subject, email, 'group11.ltw@gmail.com' , [self.user.email], fail_silently=False)
            except:
                pass


class Comment(models.Model):
    movie = models.ForeignKey(Movie,related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="publisher", on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name="comnent_like")
    unlikes = models.ManyToManyField(User,related_name="comnent_unlike")
    marks = models.ManyToManyField(User,related_name="comnent_mark")
    who_has_it_open = models.IntegerField(null=True,blank=True,default=0)

    
    #Reply cho comment
    parent = models.ForeignKey("self",blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        #cái nào mới nhất thì show trước
        ordering = ['-date_added']

    def __str__(self):
        return '%s - %s' % (self.movie.title,self.user.first_name)
    def total_likes(self):
        return self.likes.count()
    def total_unlikes(self):
        return self.unlikes.count()

    def is_like(self):
        return self.likes.filter(id=self.who_has_it_open).exists()
    def is_unlike(self):
        return self.unlikes.filter(id=self.who_has_it_open).exists()
    def is_mark(self):
        return self.marks.filter(id=self.who_has_it_open).exists()

    #subcomment
    def children(self):
        return Comment.objects.filter(parent=self)
    
    def children_count(self):
        return Comment.objects.filter(parent=self).count()
    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

class RatingStar(models.Model):
    movie = models.ForeignKey(Movie,related_name="movies", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    rate = models.IntegerField(blank=True, null=True, default=0)
    def __str__(self):
        return '%s - %s - %d' % (self.movie.title,self.user.first_name, self.rate)


# Tin hieu thong bao them user moi -> Them Profile moi
@receiver(post_save, sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=Movie)
def send_notification_to_listuser(sender,instance,created,**kwargs):
    #return HttpResponseRedirect('/log_in/')
    #raise ""
    if created:
        try: 
            tests = Profile.objects.filter(is_need_to_notify=True)
            for test in tests:
                test.send_notification(instance.title, instance.description)
            print("Succeed in mailing")
        except:
            print("Fail to mail")