# uma lista de pessoas onde cada pessoa é representada por um dictionary
people = [
    {"name": "Ewerton", "cor": "preto"},
    {"name": "Taylise", "cor": "rosa"},
    {"name": "Marwin", "cor": "marron"}
]

# Essa linha vai causa a excpetion TypeError: '<' not supported between instances of 'dict' and 'dict'
# Isso ocorre porque o phyton não sabe qual critério utilizar para comparar dois dictionaries
# people.sort() 

# para resolver a excessão é possível criar uma função que retorna a propria pessoa e usar essa função como criterio do sort()
def sortByName(person):
    return person["name"]
people.sort(key=sortByName)
print(people)

# o mesmo se aplica se eu quiser ordenar por cor
def sortByCor(person):
    return person["cor"]
people.sort(key=sortByCor)
print(people)

# Mas como essa funções que definem a ordenação (sortByName(), sortByCor()) são tão simples e usadas em apenas um lugar
# o python oferece uma maneira de defini-las "inline" chamam isso de lambda.
# em C# seria o equivalente à people.OrderBy(person => person.name)
people.sort(key=lambda person: person["name"])
print(people) # Executar isso vai dar a excessão 
