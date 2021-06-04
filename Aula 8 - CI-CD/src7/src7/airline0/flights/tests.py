from django.db.models import Max
from django.test import Client, TestCase

from .models import Airport, Flight, Passenger

# Create your tests here.
class FlightTestCase(TestCase):

    # cria uma novo database com valores ficticios para realizar os testes
    def setUp(self):

        # Create airports.
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # Create flights.
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
        Flight.objects.create(origin=a1, destination=a2, duration=-100)

    def test_departures_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)

    def test_arrivals_count(self):
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 1)

    def test_valid_flight(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight())

    def test_invalid_flight_destination(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=-100)
        self.assertFalse(f.is_valid_flight())

    def test_index(self):
        # Cria um client para simular um web request
        c = Client()
        
        # faz uma requisição para uma rota
        response = c.get("/flights/")
        print(response)
        
        # verifica o ResponseStatus
        self.assertEqual(response.status_code, 200)
        
        # response.context contem as variáveis que foram definidas na view e passadas
        # como parametro para um template html
        # No exemplo abaixo o contexto é "flights"
        #return render(request, "flights/index.html", {
        #    "flights": Flight.objects.all()
        #})
        self.assertEqual(response.context["flights"].count(), 3)

    def test_valid_flight_page(self):
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)

        c = Client()

        # Faz uma request para um flight que eu tenho certeza que existe
        response = c.get(f"/flights/{f.id}")

        # Verifica se deu Status code 200, pois o flight existe
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):
        # Descobre a maior pk que exite para a tabela Flight
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()

        # faz um request para uma pk que NÃO existe
        response = c.get(f"/flights/{max_id + 1}")
        
        # Garante que vai dar erro 404
        self.assertEqual(response.status_code, 404)

    def test_flight_page_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_non_passengers(self):
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Alice", last="Adams")

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)
