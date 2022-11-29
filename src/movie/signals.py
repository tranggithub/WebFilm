from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseRedirect
from .models import Movie
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
#Gửi thông báo nếu có film mới cho người dùng đăng ký
@receiver(post_save,sender=Movie)
def send_notification(sender, instance: Movie, **kwargs):
    pass
    # data = password_reset_form.cleaned_data['email']
    # associated_users = User.objects.filter(Q(email=data))
    # if associated_users.exists():
    #     for user in associated_users:
    #         subject = "Password Reset Requested"
    #         email_template_name = "./Info/password_reset_email.txt"
    #         c = {
    #         "email":user.email,
    #         'domain':'127.0.0.1:8000',
    #         'site_name': 'LTWFlix',
    #         "uid": urlsafe_base64_encode(force_bytes(user.pk)),
    #         "user": user,
    #         'token': default_token_generator.make_token(user),
    #         'protocol': 'http',
    #         }
    #         email = render_to_string(email_template_name, c)
    #         try:
    #             send_mail(subject, email, 'group11.ltw@gmail.com' , [user.email], fail_silently=False)
    #         except BadHeaderError:
    #             messages.error(request,"Bad header")
    #         return HttpResponse('Invalid header found.')
    #         messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
    #         return redirect ("/movies/reset_password/done")
    #     messages.error(request, 'An invalid email has been entered.')
    #     return redirect('/movies/reset_password/')
    # messages.error(request, 'An invalid email has been entered.')
    # return redirect('/movies/reset_password/')