from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"), # mostra uma lista de voos
    path("<int:flight_id>", views.flight, name="flight"), # permite ver os detalhes de detreminado voo pelo ID
    path("<int:flight_id>/book", views.book, name="book") # permite associar um passageiro à um voo
]