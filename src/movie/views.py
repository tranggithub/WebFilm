from ast import Mod
import json
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
from django.http import JsonResponse
from django.core.paginator import Paginator
#####################################
from django.views.generic.dates import YearArchiveView

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
        return redirect('sign_up')
      except User.DoesNotExist:
        nm = request.POST.get('name')
        myuser = User.objects.create_user(username=usernm,email=mail,password=passwd1)
        myuser.first_name = nm
        myuser.save()
        messages.success(request,"Your account has been created successfully")
        return redirect('log_in')
    else:
      messages.error(request,"Your confirm password and your password are not the same")
      return redirect('sign_up')
  return render(request,"./SignUp_LogIn/SignUpFilm.html")


def LogIn(request):
  if request.user.is_authenticated:
    messages.warning(request, "You have already logged in")
    return redirect('userpacket')
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
        return redirect('userpacket')
      else:
        messages.error(request,"Invalid Username or Password")
        return redirect('log_in')
    
    movie = Movie.objects.all()

    #Số movie mỗi trang
    movies_per_page = 1

    #Số lượng movie xuất hiện là 4
    movie_paginator = Paginator(movie,movies_per_page)
    #Lấy số trang từ request
    m_num = request.GET.get('m_num')
    #Chỉ định list trang muốn lấy ở trang nào
    movie_page = movie_paginator.get_page(m_num)
    return render(request,"./SignUp_LogIn/LoginFilm.html",{'movie_page':movie_page})

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
      return redirect('reset_password')
    messages.error(request, 'An invalid email has been entered.')
    return redirect('reset_password')

  password_reset_form = PasswordResetForm()
  return render(request, template_name="./Info//reset_password.html", context={"form":password_reset_form})

Choices_User="CHILD"
 

@login_required(login_url='log_in')
def Home(request):
  if request.method == "POST":
    url='/movies/home/'
    if 'notify' in request.POST:
      if request.user.profile.is_need_to_notify == False:
        if request.user.email is not None:
          request.user.profile.is_need_to_notify = True
          request.user.profile.save()
          messages.success(request,"You will reveive emails if we add new movie")
          redirect(url)
        else:
          messages.error(request,"You don't have an email in your account")
          redirect(url)
      else:
        request.user.profile.is_need_to_notify = False
        request.user.profile.save()
        messages.success(request,"You won't receive any emails when we add new movie")
        redirect(url)
    
  profile = Profile.objects.get(user=request.user)
  ava = request.user.profile.avatar.url
  if Choices_User=="CHILD":
    movies = Movie.objects.filter(child='Yes')
    trending = Movie.objects.filter(status__status='T',child='Yes')[:4]
    upcoming = Movie.objects.filter(status__status='U',child='Yes')[:4]
    tv_series = Movie.objects.filter(format='TV',child='Yes')[:4]
    ps = Movie.objects.filter(format='PS',child='Yes')[:4]
    return render(request,"Home/Home.html",{'avatar':ava, 'movies': movies,'trending': trending, 'upcoming':upcoming, 'tv_series':tv_series, 'ps':ps,'profile':profile})
  else:
    movies = Movie.objects.all()
    trending = Movie.objects.filter(status__status='T')[:4]
    upcoming = Movie.objects.filter(status__status='U')[:4]
    tv_series = Movie.objects.filter(format='TV')[:4]
    ps = Movie.objects.filter(format='PS')[:4]
    return render(request,"Home/Home.html",{'avatar':ava, 'movies': movies,'trending': trending, 'upcoming':upcoming, 'tv_series':tv_series, 'ps':ps, 'profile':profile})

@login_required(login_url='log_in')
def UserPacket(request):
  global Choices_User
  if request.method=='POST':
    Choices_User=request.POST.get('Child')  
    return redirect ('home')
  else:    
    return render(request,'UserPacket/Service_pack.html')
 
  
@login_required(login_url='log_in')
def SeeAll_Trending(request, status_short):
  if request.method == "POST":
    url='/movies/seeall_trending_english/' + status_short
    if 'notify' in request.POST:
      if request.user.profile.is_need_to_notify == False:
        if request.user.email is not None:
          request.user.profile.is_need_to_notify = True
          request.user.profile.save()
          messages.success(request,"You will reveive emails if we add new movie")
          redirect(url)
        else:
          messages.error(request,"You don't have an email in your account")
          redirect(url)
      else:
        request.user.profile.is_need_to_notify = False
        request.user.profile.save()
        messages.success(request,"You won't receive any emails when we add new movie")
        redirect(url)
  if status_short == 'U':
    title = "Upcomming"
  elif status_short == 'T':
    title = "Trending"
  elif status_short == 'TV':
    title = "TV Series"
  else:
    title = "Popular Movies On September"
  profile=Profile.objects.get(user=request.user) 
  if status_short == 'U' or status_short =='T':
    if Choices_User=="CHILD":
      ava = request.user.profile.avatar.url
      movies = Movie.objects.filter(status__status=status_short,child='Yes')
      return render(request,"./Home/SeeAll_Trending_English.html",{'avatar':ava, 'movies':movies, 'title':title,'profile':profile})
    else: 
      ava = request.user.profile.avatar.url
      movies = Movie.objects.filter(status__status=status_short)
      return render(request,"./Home/SeeAll_Trending_English.html",{'avatar':ava, 'movies':movies, 'title':title,'profile':profile})
  else:
    if Choices_User=="CHILD":
      ava = request.user.profile.avatar.url
      movies = Movie.objects.filter(format=status_short,child='Yes')
      return render(request,"./Home/SeeAll_Trending_English.html",{'avatar':ava, 'movies':movies, 'title':title,'profile':profile})
    else: 
      ava = request.user.profile.avatar.url
      movies = Movie.objects.filter(format=status_short)
      return render(request,"./Home/SeeAll_Trending_English.html",{'avatar':ava, 'movies':movies, 'title':title,'profile':profile})



def Loading_Circle(request):
  template = loader.get_template('./Loading_Screen_Logo/loading_screen.html')
  return HttpResponse(template.render())

def Loading_Logo(request):
  template = loader.get_template('./Loading_Screen_Logo/sign_up.html')
  return HttpResponse(template.render())

@login_required(login_url='log_in')
def LogOut(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Log out successfully")
    return redirect('/movies/log_in')
  else:
    messages.error(request,"Log out failed")
    return redirect('/movies/log_in')

@login_required(login_url='log_in')
def Movies(request):
  if request.method == "POST":
    url='/movies/movies/'
    if 'notify' in request.POST:
      if request.user.profile.is_need_to_notify == False:
        if request.user.email is not None:
          request.user.profile.is_need_to_notify = True
          request.user.profile.save()
          messages.success(request,"You will reveive emails if we add new movie")
          redirect(url)
        else:
          messages.error(request,"You don't have an email in your account")
          redirect(url)
      else:
        request.user.profile.is_need_to_notify = False
        request.user.profile.save()
        messages.success(request,"You won't receive any emails when we add new movie")
        redirect(url)
  profile=Profile.objects.get(user=request.user)  
  if  Choices_User=="CHILD":
    ava = request.user.profile.avatar.url
    movies = Movie.objects.filter(child='Yes')[:4]
    upcoming = Movie.objects.filter(status__status='U',child='Yes')[:4]
    tv_series = Movie.objects.filter(format='TV',child='Yes')[:4]
    ps = Movie.objects.filter(format='PS',child='Yes')[:4]
    

    return render(request,"Movies/movies.html",{'avatar':ava, 'movies': movies, 'upcoming':upcoming, 'tv_series':tv_series, 'ps':ps,'profile':profile})

  else:
    ava = request.user.profile.avatar.url
    movies = Movie.objects.all()[:4]
    upcoming = Movie.objects.filter(status__status='U')[:4]
    tv_series = Movie.objects.filter(format='TV')[:4]
    ps = Movie.objects.filter(format='PS')[:4]
    
    return render(request,"Movies/movies.html",{'avatar':ava, 'movies': movies, 'upcoming':upcoming, 'tv_series':tv_series, 'ps':ps,'profile':profile})

@login_required(login_url='log_in')
def Library(request):
 
  if request.method == "POST":
    url='/movies/library/'
    if 'notify' in request.POST:
      if request.user.profile.is_need_to_notify == False:
        if request.user.email is not None:
          request.user.profile.is_need_to_notify = True
          request.user.profile.save()
          messages.success(request,"You will reveive emails if we add new movie")
          redirect(url)
        else:
          messages.error(request,"You don't have an email in your account")
          redirect(url)
      else:
        request.user.profile.is_need_to_notify = False
        request.user.profile.save()
        messages.success(request,"You won't receive any emails when we add new movie")
        redirect(url)
  profile=Profile.objects.get(user=request.user)
  if Choices_User=="CHILD":
    ava = request.user.profile.avatar.url
  
    love = Movie.objects.filter(loves__id=request.user.id,child='Yes')
    mark = Movie.objects.filter(marks__id=request.user.id,child='Yes')
    history = Movie.objects.filter(history__id=request.user.id,child='Yes')

    #Số movie mỗi trang
    movies_per_page = 4

    #Số lượng movie xuất hiện là 4
    love_paginator = Paginator(love,movies_per_page)
    #Lấy số trang từ request
    l_num = request.GET.get('l_num')
    #Chỉ định list trang muốn lấy ở trang nào
    love_page = love_paginator.get_page(l_num)


    mark_paginator = Paginator(mark,movies_per_page)
    m_num = request.GET.get('m_num')
    mark_page = mark_paginator.get_page(m_num)

    history_paginator = Paginator(history,movies_per_page)
    h_num = request.GET.get('h_num')
    history_page = history_paginator.get_page(h_num)
    movies = Movie.objects.filter(child='Yes')
    context = {
    'avatar':ava, 
    'movies': movies,
    'love_page': love_page,
    'mark_page': mark_page,
    'history_page': history_page,
    'profile':profile
    }
    return render(request,"./Trailer_Detail/Library.html",context)

  else: 
    ava = request.user.profile.avatar.url  
    love = Movie.objects.filter(loves__id=request.user.id)
    mark = Movie.objects.filter(marks__id=request.user.id)
    history = Movie.objects.filter(history__id=request.user.id)

    #Số movie mỗi trang
    movies_per_page = 4

    #Số lượng movie xuất hiện là 4
    love_paginator = Paginator(love,movies_per_page)
    #Lấy số trang từ request
    l_num = request.GET.get('l_num')
    #Chỉ định list trang muốn lấy ở trang nào
    love_page = love_paginator.get_page(l_num)


    mark_paginator = Paginator(mark,movies_per_page)
    m_num = request.GET.get('m_num')
    mark_page = mark_paginator.get_page(m_num)

    history_paginator = Paginator(history,movies_per_page)
    h_num = request.GET.get('h_num')
    history_page = history_paginator.get_page(h_num)
    movies = Movie.objects.all()  
    context = {
    'avatar':ava, 
    'movies': movies,
    'love_page': love_page,
    'mark_page': mark_page,
    'history_page': history_page,
    'profile':profile
      }
  return render(request,"./Trailer_Detail/Library.html",context)

@login_required(login_url='log_in')
def WatchFilm(request, movie_id, number_ep):
  if request.user.is_authenticated:
    movie = Movie.objects.get(pk=movie_id)
    for comment in movie.comments.all():
      comment.who_has_it_open = request.user.id
      comment.save()
    ep = get_object_or_404(Episode,title__id=movie_id,number_episode=number_ep)
    if movie.history.filter(id=request.user.id).exists():
      pass
    else:
      movie.history.add(request.user)
    if request.method == "POST":
      url = '/movies/watch/'+ movie_id + "/" + number_ep
      if 'comment' in request.POST:
        usr = request.user
        comment = request.POST.get('comment')
        try:
          cmt = Comment.objects.create(movie=movie,user=usr,body=comment)
          cmt.save()
        except:
          messages.error(request,"Fail to comment")
          return redirect(url)
        messages.success(request,"Comment successfully")
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
        return redirect(url)
      elif 'unlike' in request.POST:
        value = request.POST.get('unlike')
        comment = Comment.objects.get(pk=value)
        if comment.unlikes.filter(id=request.user.id).exists():
          comment.unlikes.remove(request.user)
        else:
          comment.likes.remove(request.user)
          comment.unlikes.add(request.user)
        return redirect(url)
      elif 'mark' in request.POST:
        value = request.POST.get('mark')
        comment = Comment.objects.get(pk=value)
        if comment.marks.filter(id=request.user.id).exists():
          comment.marks.remove(request.user)
        else:
          comment.marks.add(request.user)
        return redirect(url)
      elif 'subcomment_icon' in request.POST:
        value = request.POST.get('subcomment_icon')
        comment = Comment.objects.get(pk=value)
        if comment.reply.filter(id=request.user.id).exists():
          comment.reply.remove(request.user)
        else:
          comment.reply.add(request.user)
        return redirect(url)
      elif 'star1' in request.POST:
        if RatingStar.objects.filter(movie__id=movie_id, user__id=request.user.id).exists():
          myrate = RatingStar.objects.get(movie__id=movie_id, user__id=request.user.id)
          myrate.rate = 1
          myrate.save()
        else:
          usr = request.user
          myrate = RatingStar.objects.create(user=usr,movie=movie,rate=1)
          myrate.save()
        return redirect(url)
      elif 'star2' in request.POST:
        if RatingStar.objects.filter(movie__id=movie_id, user__id=request.user.id).exists():
          myrate = RatingStar.objects.get(movie__id=movie_id, user__id=request.user.id)
          myrate.rate = 2
          myrate.save()
        else:
          usr = request.user
          myrate = RatingStar.objects.create(user=usr,movie=movie,rate=2)
          myrate.save()
        return redirect(url)
      elif 'star3' in request.POST:
        if RatingStar.objects.filter(movie__id=movie_id, user__id=request.user.id).exists():
          myrate = RatingStar.objects.get(movie__id=movie_id, user__id=request.user.id)
          myrate.rate = 3
          myrate.save()
        else:
          usr = request.user
          myrate = RatingStar.objects.create(user=usr,movie=movie,rate=3)
          myrate.save()
        return redirect(url)
      elif 'star4' in request.POST:
        if RatingStar.objects.filter(movie__id=movie_id, user__id=request.user.id).exists():
          myrate = RatingStar.objects.get(movie__id=movie_id, user__id=request.user.id)
          myrate.rate = 4
          myrate.save()
        else:
          usr = request.user
          myrate = RatingStar.objects.create(user=usr,movie=movie,rate=4)
          myrate.save()
        return redirect(url)
      elif 'star5' in request.POST:
        if RatingStar.objects.filter(movie__id=movie_id, user__id=request.user.id).exists():
          myrate = RatingStar.objects.get(movie__id=movie_id, user__id=request.user.id)
          myrate.rate = 5
          myrate.save()
        else:
          usr = request.user
          myrate = RatingStar.objects.create(user=usr,movie=movie,rate=5)
          myrate.save()
        return redirect(url)
      elif 'notify' in request.POST:
        if request.user.profile.is_need_to_notify == False:
          if request.user.email is not None:
            request.user.profile.is_need_to_notify = True
            request.user.profile.save()
            messages.success(request,"You will reveive emails if we add new movie")
            redirect(url)
          else:
            messages.error(request,"You don't have an email in your account")
            redirect(url)
        else:
          request.user.profile.is_need_to_notify = False
          request.user.profile.save()
          messages.success(request,"You won't receive any emails when we add new movie")
          redirect(url)
          return redirect(url)
      elif 'subcomment' in request.POST:
        parent_id=request.POST.get('comment_id')
        usr = request.user
        comment = request.POST.get('subcomment')
        parent_obj = None
        try:
          parent_obj = Comment.objects.get(id=parent_id)
        except:
          parent_obj = None

        try:
          cmt = Comment.objects.create(movie=movie,user=usr,body=comment,parent=parent_obj)
          cmt.save()
        except:
          messages.error(request,"Fail to comment")
          return redirect(url)
        messages.success(request,"Comment successfully")
        return redirect(url)
    try: 
      myrate = RatingStar.objects.get(movie__id=movie_id, user__id=request.user.id)
      rate = myrate.rate
    except:
      rate = 0
    profile = Profile.objects.get(user=request.user)
    ava = request.user.profile.avatar.url
    movies = Movie.objects.filter(id=movie_id)
    user = request.user
    episode = movies.get().movie_episode.all()
    # get_ep = episode.filter(number_episode=number_ep)
    ep = get_object_or_404(Episode, title__id=movie_id, number_episode=number_ep)
    # value = request.GET.get('like')
    # try:
    #   comment = Comment.objects.get(pk=value)
    # except:
    #   return HttpResponseRedirect(reverse('watch', args=[str(movie_id)]))
    # if comment.likes.filter(id=request.user.id).exists():
    #   like = True
    # else:
    #   like = False

    return render(request,"./Trailer_Detail/Watch.html",{
        'avatar':ava, 
        'movies': movies, 
        'episode': episode, 
        'ep': ep,
        'user':user,
        'rate' : rate,
        'ep': ep,
        'profile': profile
        })
  else:
    messages.error(request,"Please log in!")
    url=reverse_lazy('log_in')
    redirect(url)

@login_required(login_url='log_in')
def Detail(request, movie_id):
  if request.method == "POST":
    url='movies/detail/' + movie_id
    if 'notify' in request.POST:
      if request.user.profile.is_need_to_notify == False:
        if request.user.email is not None:
          request.user.profile.is_need_to_notify = True
          request.user.profile.save()
          messages.success(request,"You will reveive email if we add new movie")
          redirect(url)
        else:
          messages.error(request,"You don't have an email in your account")
          redirect(url)
      else:
        request.user.profile.is_need_to_notify = False
        request.user.profile.save()
        messages.success(request,"You won't reveive email when we add new movie")
        redirect(url)

  if  Choices_User=="CHILD": 
    #movie = get_object_or_404(Movie,id=movie_id)
    movie = Movie.objects.get(pk=movie_id)
    movie.who_has_it_open = request.user.id
    movie.save()
    if request.method == "POST":
      if 'love' in request.POST:
        #comment = get_object_or_404(Comment, id=request.POST.get('like'))
        movie = Movie.objects.get(pk=movie_id)
        if movie.loves.filter(id=request.user.id).exists():
          movie.loves.remove(request.user)
        else:
          movie.loves.add(request.user)
        return HttpResponseRedirect(reverse('detail', args=[str(movie_id)]))
      elif 'mark' in request.POST:
        if movie.marks.filter(id=request.user.id).exists():
          movie.marks.remove(request.user)
        else:
          movie.marks.add(request.user)
        url = '/movies/detail/'+ movie_id
        return redirect(url)
    profile = Profile.objects.get(user=request.user)
    ava = request.user.profile.avatar.url
    another = Movie.objects.filter(child='Yes').exclude(id=movie_id)[:4]
    movies = Movie.objects.filter(id=movie_id,child='Yes')
    category = movies.get().categories.all()
    cast_crew = movies.get().cast_and_crew.all()
    topcast = movies.get().cast_and_crew.all()[:4]
    return render(request,"./Trailer_Detail/Trailer_Detail.html",
    {'avatar':ava, 
    'another': another, 
    'movies': movies, 
    'categories': category,
    'topcast': topcast, 
    'cast_crew': cast_crew,
  'profile': profile})
  else:
    #movie = get_object_or_404(Movie,id=movie_id)
    movie = Movie.objects.get(pk=movie_id)
    movie.who_has_it_open = request.user.id
    movie.save()
    if request.method == "POST":
      if 'love' in request.POST:
        #comment = get_object_or_404(Comment, id=request.POST.get('like'))
        movie = Movie.objects.get(pk=movie_id)
        if movie.loves.filter(id=request.user.id).exists():
          movie.loves.remove(request.user)
        else:
          movie.loves.add(request.user)
        return HttpResponseRedirect(reverse('detail', args=[str(movie_id)]))
      elif 'mark' in request.POST:
        if movie.marks.filter(id=request.user.id).exists():
          movie.marks.remove(request.user)
        else:
          movie.marks.add(request.user)
        url = '/movies/detail/'+ movie_id
        return redirect(url)
  profile = Profile.objects.get(user=request.user)
  ava = request.user.profile.avatar.url
  another = Movie.objects.all().exclude(id=movie_id)[:4]
  movies = Movie.objects.filter(id=movie_id)
  category = movies.get().categories.all()
  cast_crew = movies.get().cast_and_crew.all()
  topcast = movies.get().cast_and_crew.all()[:4]
  return render(request,"./Trailer_Detail/Trailer_Detail.html",
  {'avatar':ava, 
  'another': another, 
  'movies': movies, 
  'categories': category,
  'topcast': topcast, 
  'cast_crew': cast_crew,
  'profile': profile})




class UserForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ("first_name","email")

class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ("avatar","birthday","gender")

@login_required(login_url='log_in')
def Info(request):
  nm = request.user.first_name
  mail = request.user.email
  sex = request.user.profile.get_gender_display
  ava = request.user.profile.avatar.url
  bd = request.user.profile.birthday
  return render(request,"./Info/info.html",{'name':nm, 'email':mail, 'gender':sex,'avatar':ava,'birthday':bd})

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
      return redirect('info')
    else:
      messages.error(request,"Invalid value")
  else:
    user_form = UserForm(instance=request.user)
    user_profile_form = ProfileForm(instance=request.user.profile)
  return render(request,'./Info/change_info.html',{'u_form':user_form, 'p_form':user_profile_form}) 

@login_required(login_url='log_in')
def searchBar(request):
  if request.method == "POST":
    url='/movies/search/'
    if 'notify' in request.POST:
      if request.user.profile.is_need_to_notify == False:
        if request.user.email is not None:
          request.user.profile.is_need_to_notify = True
          request.user.profile.save()
          messages.success(request,"You will reveive emails if we add new movie")
          redirect(url)
        else:
          messages.error(request,"You don't have an email in your account")
          redirect(url)
      else:
        request.user.profile.is_need_to_notify = False
        request.user.profile.save()
        messages.success(request,"You won't receive any emails when we add new movie")
        redirect(url)
  profile = Profile.objects.get(user=request.user)  
  if  Choices_User=="CHILD": 
    # profile=Profile.objects.get(user=request.user)
    keyword=request.GET['keyword']
    ava = request.user.profile.avatar.url 
    movies = Movie.objects.filter(title__contains=keyword,child='Yes')   
    Toprated = Movie.objects.filter(status__status='TR',child='Yes')[:4]
    Mostwatch = Movie.objects.filter(status__status='MW',child='Yes')[:4]
    return render(request,"./Search/Searchbar.html",{'avatar':ava, 'movies':movies, 'Toprated':Toprated, 'Mostwatch':Mostwatch})
  else:
    # profile=Profile.objects.get(user=request.user)
    keyword=request.GET['keyword']
    ava = request.user.profile.avatar.url 
    movies = Movie.objects.filter(title__contains=keyword)   
    Toprated = Movie.objects.filter(status__status='TR')[:4]
    Mostwatch = Movie.objects.filter(status__status='MW')[:4]
    return render(request,"./Search/Searchbar.html",{'avatar':ava, 'movies':movies, 'Toprated':Toprated, 'Mostwatch':Mostwatch})

# def searchBar_auto(request):
#    keyword= request.GET.get('keyword')
#    movies=Movie.objects.filter(title__icontains=keyword)
#    movie=[]
#    movie+= [x.title for x in movies]
#    return JsonResponse(movie,safe=False)
    
      
  
  # return HttpResponse(template.render())


# def ChangePassword(request):
#   template = loader.get_template('./Info/change_password.html')
#   return HttpResponse(template.render())
def handler404(request, exception):
    return render(request,'Not_found_404.html')




# def HomeChild(request):
#   if request.method == "POST":
#     url='/movies/homechild/'
#     if 'notify' in request.POST:
#       if request.user.profile.is_need_to_notify == False:
#         if request.user.email is not None:
#           request.user.profile.is_need_to_notify = True
#           request.user.profile.save()
#           messages.success(request,"You will reveive email if we add new movie")
#           redirect(url)
#         else:
#           messages.error(request,"You don't have an email in your account")
#           redirect(url)
#       else:
#         request.user.profile.is_need_to_notify = False
#         request.user.profile.save()
#         messages.success(request,"You won't reveive email when we add new movie")
#         redirect(url)
 
# def Movies_Child(request):
#     

class SeeAll_Trending_Filer(ListView):
    model = Movie
    template_name = './Home/SeeAll_Trending_Filter.html'

class MovieNational(ListView):
      model=Movie
      paginate_by = 10
      template_name = './Home/SeeAll_Trending_Filter.html'           
      def get_queryset(self):
        if  Choices_User=="CHILD": 
          self.national=self.kwargs['Nation']   
          return Movie.objects.filter(national=self.national,child='Yes')
        else: 
          self.national=self.kwargs['Nation']   
          return Movie.objects.filter(national=self.national)

      def get_context_data(self, **kwargs):
        context=super(MovieNational , self).get_context_data(**kwargs)
        context['movie_national']=self.national
        context['avatar']=self.request.user.profile.avatar.url
        context['profile']=Profile.objects.get(user=self.request.user)
        return context
    


class MovieFormat(ListView):
  
  
    model=Movie
    paginate_by = 5
    template_name = './Home/SeeAll_Trending_Filter.html'
    def get_queryset(self):
      if  Choices_User=="CHILD": 
        self.format=self.kwargs['for']
        return Movie.objects.filter(format=self.format,child='Yes')
      else:
        self.format=self.kwargs['for']
        return Movie.objects.filter(format=self.format)
    def get_context_data(self, **kwargs):
      context=super(MovieFormat , self).get_context_data(**kwargs)
      context['movie_format']=self.format
      context['avatar']=self.request.user.profile.avatar.url
      context['profile']=Profile.objects.get(user=self.request.user)
      return context
  
class MovieSort(ListView):
  
  
    model=Movie
    paginate_by = 5
    template_name = './Home/SeeAll_Trending_Filter.html'
    def get_queryset(self):
      if  Choices_User=="CHILD": 
        self.sort=self.kwargs['so']
        return Movie.objects.filter(sort=self.sort,child='Yes')
      else:
        self.sort=self.kwargs['so']
        return Movie.objects.filter(sort=self.sort)

    def get_context_data(self, **kwargs):
      context=super(MovieSort , self).get_context_data(**kwargs)
      context['movie_sort']=self.sort
      context['avatar']=self.request.user.profile.avatar.url
      context['profile']=Profile.objects.get(user=self.request.user)
      return context
  
class MovieCondition(ListView):
  
  
    model=Movie
    paginate_by = 5
    template_name = './Home/SeeAll_Trending_Filter.html'
    def get_queryset(self):
      if  Choices_User=="CHILD": 
        self.condition =self.kwargs['condi']
        return Movie.objects.filter(condition =self.condition,child='Yes')
      else:
        self.condition =self.kwargs['condi']
        return Movie.objects.filter(condition =self.condition)

    def get_context_data(self, **kwargs):
      context=super(MovieCondition , self).get_context_data(**kwargs)
      context['movie_condition']=self.condition
      context['avatar']=self.request.user.profile.avatar.url
      context['profile']=Profile.objects.get(user=self.request.user)
      return context
  


class MovieYear(ListView):
  
 
    model=Movie
    paginate_by = 5
    template_name = './Home/SeeAll_Trending_Filter.html'
    def get_queryset(self):
      if  Choices_User=="CHILD": 
        self.year=self.kwargs['year']
        return Movie.objects.filter(year_of_production__contains=self.year,child='Yes')
      else:
        self.year=self.kwargs['year']
        return Movie.objects.filter(year_of_production__contains=self.year)

    def get_context_data(self, **kwargs):
      context=super(MovieYear , self).get_context_data(**kwargs)
      context['movie_year']=self.year
      context['avatar']=self.request.user.profile.avatar.url
      context['profile']=Profile.objects.get(user=self.request.user)
      return context
 

class MovieCategory(ListView):
  model=Movie
  paginate_by = 5
  template_name = './Home/SeeAll_Trending_Filter.html'
  
  def get_queryset(self):
      if  Choices_User=="CHILD": 
        self.category=self.kwargs['cate']
        return Movie.objects.filter(categories__category=self.category,child='Yes')
      else: 
        self.category=self.kwargs['cate']
        return Movie.objects.filter(categories__category=self.category)
  def get_context_data(self, **kwargs):
      context=super(MovieCategory , self).get_context_data(**kwargs)
      context['movie_category']=self.category
      context['avatar']=self.request.user.profile.avatar.url
      context['profile']=Profile.objects.get(user=self.request.user)
      return context
  