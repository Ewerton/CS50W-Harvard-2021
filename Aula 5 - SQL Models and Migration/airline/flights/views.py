from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Flight, Passenger

# Create your views here.
def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })


def flight(request, flight_id):
    # pk é uam maneira generica de se referenciar o pk do banco
    flight = Flight.objects.get(pk=flight_id)
    np = Passenger.objects.exclude(flights=flight).all()
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": np
    })


def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)

        # assume que o passanger vai ser um campo do FORM postado chamado "passenger"
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        
        # adiciona o passageiro ao Voo
        passenger.flights.add(flight)

        # redireciona para a URL do Voo específico. A rota flight aceita um argumento então eu passo o Id do Voo.
        #reverse pega o nome de uma view e retorna a URL a qual aquele nome pertence.
        return HttpResponseRedirect(reverse("flight", args=[flight.id]))