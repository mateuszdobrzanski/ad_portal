from django.urls import path, reverse_lazy
# from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from . import views

# app_name = 'accounts'

urlpatterns = [

    # path('login/', LoginView.as_view(template_name='accounts/login.html'), name="login"),
    # changed login method, rename folder 'templates/accounts' to 'templates/registration'
    # if user is authenticated, we will redirect user from login page to main site
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),

    path('password_change/', auth_views.PasswordChangeView.as_view(), name="password_change"),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),

    # this fix error Reverse for 'password_reset_done' not found.
    # 'password_reset_done' is not a valid view function or pattern name.
    # this works with path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')) at main urls.py
    path('password_reset/', auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('accounts:password_reset_done',)
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('accounts:password_reset_complete')
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # route to sign up new users
    path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # account detail/ user profile
    path('profile/', views.account_detail, name='account_profile'),
    path('profile/change_details/', views.change_details, name='account_change_details')

]
