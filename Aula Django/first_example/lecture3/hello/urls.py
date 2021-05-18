from django.urls import path
from . import views  # Do diretorio atual (.) importe o arquivo views.py

urlpatterns = [
    path("", views.index, name="index"),
    # path("ewerton", views.ewerton, name="ewerton"),
    # path("taylise", views.ewerton, name="taylise"),
    # path("marwin", views.ewerton, name="marwin"),
    path("<str:name>", views.greet, name="greet") # quando tiver uma url que tem uma string, chame a view "greet"
]