class Flight():
    def __init__(self, capacity):
        self.capacity = capacity  # capacidade de pessoas no voo
        self.passangers = []  # cria uma lista vazia de passageiros

    def add_passenger(self, name):
        if not self.open_seats():  # Se NÃO houver acentos disponiveis
            return False
        self.passangers.append(name)
        return True

    def open_seats(self):
        return self.capacity - len(self.passangers)


fligt = Flight(3)

people = ["Ewerton", "Taylise", "Marwin", "Daniel"]
for person in people:
    if fligt.add_passenger(person):
        print(f"Added {person} to flight successfuly")
    else:
        print(f"No available seats for {person} ")
