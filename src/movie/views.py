from ast import Mod
from django.http import HttpResponse, HttpResponseRedirect
from pyexpat import model
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth import views as auth_views
# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Movie, Profile
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.core.mail import send_mail, BadHeaderError
from .models import *
from django.urls import reverse_lazy, reverse
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
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(360) #6 phút
        else:
            request.session.set_expiry(2592000)#30 ngày
        login(request, user)
        messages.success(request,"Log in successfully")
        return redirect('/movies/userpacket')
      else:
        messages.error(request,"Invalid Username or Password")
        return redirect('/movies/log_in')
    return render(request,".\SignUp_LogIn\LogInFilm.html")

def password_reset_request(request):
  if request.method == "POST":
    password_reset_form = PasswordResetForm(request.POST)
    if password_reset_form.is_valid():
      data = password_reset_form.cleaned_data['email']
      associated_users = User.objects.filter(Q(email=data))
      if associated_users.exists():
        for user in associated_users:
          subject = "Password Reset Requested"
          email_template_name = "./Info/password_reset_email.txt"
          c = {
            "email":user.email,
            'domain':'127.0.0.1:8000',
            'site_name': 'LTWFlix',
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "user": user,
            'token': default_token_generator.make_token(user),
            'protocol': 'http',
          }
          email = render_to_string(email_template_name, c)
          try:
            send_mail(subject, email, 'group11.ltw@gmail.com' , [user.email], fail_silently=False)
          except BadHeaderError:
            messages.error(request,"Bad header")
            return HttpResponse('Invalid header found.')
          messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
          return redirect ("/movies/reset_password/done")
      messages.error(request, 'An invalid email has been entered.')
      return redirect('/movies/reset_password/')
    messages.error(request, 'An invalid email has been entered.')
    return redirect('/movies/reset_password/')

  password_reset_form = PasswordResetForm()
  return render(request, template_name=".\Info\\reset_password.html", context={"form":password_reset_form})

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
  else:
    messages.error(request,"Log out failed")
    return redirect('/movies/log_in')


def Movies(request):
  ava = request.user.profile.avatar.url
  movies = Movie.objects.all()[:4]
  upcoming = Movie.objects.filter(status__status='U')[:4]
  tv_series = Movie.objects.filter(format='TV')[:4]
  ps = Movie.objects.filter(format='PS')[:4]
  return render(request,"Movies/movies.html",{'avatar':ava, 'movies': movies, 'upcoming':upcoming, 'tv_series':tv_series, 'ps':ps})

def WatchFilm(request, movie_id):
  if request.user.is_authenticated:
    movie = Movie.objects.get(pk=movie_id)
    if request.method == "POST":
      if 'comment' in request.POST:
        usr = request.user
        comment = request.POST.get('comment')
        try:
          cmt = Comment.objects.create(movie=movie,user=usr,body=comment)
          cmt.save()
        except:
          messages.error(request,"Fail to comment")
          url = '/movies/watch/'+ movie_id
          return redirect(url)
        messages.success(request,"Comment successfully")
        url = '/movies/watch/'+ movie_id
        return redirect(url)
      elif 'like' in request.POST:
        #comment = get_object_or_404(Comment, id=request.POST.get('like'))
        value = request.POST.get('like')
        comment = Comment.objects.get(pk=value)
        if comment.likes.filter(id=request.user.id).exists():
          comment.likes.remove(request.user)
        else:
          comment.unlikes.remove(request.user)
          comment.likes.add(request.user)
        return HttpResponseRedirect(reverse('watch', args=[str(movie_id)]))
      elif 'unlike' in request.POST:
        value = request.POST.get('unlike')
        comment = Comment.objects.get(pk=value)
        if comment.unlikes.filter(id=request.user.id).exists():
          comment.unlikes.remove(request.user)
        else:
          comment.likes.remove(request.user)
          comment.unlikes.add(request.user)
        url = '/movies/watch/'+ movie_id
        return redirect(url)
    ava = request.user.profile.avatar.url
    movies = Movie.objects.filter(id=movie_id)
    user = request.user
    episode = movies.get().movie_episode.all()
    for comment in movie.comments.all():
      comment.who_has_it_open = request.user.id
      comment.save()
    # value = request.GET.get('like')
    # try:
    #   comment = Comment.objects.get(pk=value)
    # except:
    #   return HttpResponseRedirect(reverse('watch', args=[str(movie_id)]))
    # if comment.likes.filter(id=request.user.id).exists():
    #   like = True
    # else:
    #   like = False

    return render(request,".\Trailer_Detail\Watch.html",{
        'avatar':ava, 
        'movies': movies, 
        'episode': episode, 
        'user':user,
        })
  else:
    messages.error(request,"Please log in!")
    url=reverse_lazy('log_in')
    redirect(url)

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
