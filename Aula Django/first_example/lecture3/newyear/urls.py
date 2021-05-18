from django.urls import path
from . import views  # Do diretorio atual (.) importe o arquivo views.py

urlpatterns = [
    path("", views.index, name="index")
]