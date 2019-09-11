from django.urls import path 
from . import views 
from django.contrib.auth import views as auth_views

app_name='account'
urlpatterns = [ 
    path('login/', views.user_login, name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name="account/password_change_form.html", success_url="/account/password-change-done/"), name='password_change'), 
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(template_name="account/password_change_done.html"), name='password_change_done'),
    path('register/', views.register, name='register'),
]