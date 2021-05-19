from django.db import models

# Create your models here.

class Airport(models.Model):
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.city} ({self.code})"


class Flight(models.Model):
    #origin = models.CharField(max_length=64)
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures") # Isso vai criar a colunas origin_id na tabela Flights
    
    #destination = models.CharField(max_length=64)
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals") # Isso vai criar a colunas destination_id na tabela Flights

    duration = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.origin} to {self.destination}"