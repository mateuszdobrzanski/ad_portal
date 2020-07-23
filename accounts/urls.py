from django.urls import path
# from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

# app_name = 'accounts'

urlpatterns = [

    # path('login/', LoginView.as_view(template_name='accounts/login.html'), name="login"),
    # changed login method, rename folder 'templates/accounts' to 'templates/registration'
    path('login/', auth_views.LoginView.as_view()),

]
