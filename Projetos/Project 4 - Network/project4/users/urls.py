
from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('login',views.login_view, name='login'),
    path('logout',views.logout_view, name='logout'),
    path('register/', views.register, name='register-users'),
    path('settings/', views.settings, name='settings'),
    path('search/', views.SearchView, name='search'),
]
