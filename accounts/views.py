from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from datetime import date, datetime


# here is signup form
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('registration/signup_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request,
                  'registration/signup.html',
                  {'form': form})


# when someone click activation link,
# variable is_active change status to true, and user can login
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


# show user profile
@login_required(login_url="/accounts/login")
def account_detail(request):
    # get logged user data
    user = request.user

    # here we count days from user signed up
    # we must convert date (from var date_now) and delete info about timezone for user_join_date
    user_join_date = user.date_joined
    # delete information about timezone
    user_join_date = user_join_date.replace(tzinfo=None)
    # converting date
    date_now = datetime.combine(date.today(), datetime.min.time())

    diff_date = date_now - user_join_date
    user_date = str(diff_date.days)

    context = {'date': user_date}

    template = 'registration/account_details.html'
    return render(request,
                  template,
                  context)


# change user details
@login_required(login_url="/accounts/login")
def change_details(request):
    # get logged user data
    user = request.user

    if request.method == 'POST':
        if request.POST['first_name'] and request.POST['last_name']:

            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            return redirect('/accounts/profile/')
        else:
            return render(request, 'registration/change_account_details.html', {'error': 'All fields are required'})

    context = {'user': user}
    template = 'registration/change_account_details.html'

    return render(request,
                  template,
                  context)
