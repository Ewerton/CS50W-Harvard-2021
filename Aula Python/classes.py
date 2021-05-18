class Point():
    def __init__(self, xPoint, yPoint): #construtor da classe, smpre precisa passar o self que é uma especie de referencia para o proprio objeto
        self.x = xPoint # Cria uma propriedade "x" de forma implicita
        self.y = yPoint # Cria uma propriedade "y" de forma implicita


p = Point(2,8) # Cria um novo Point
print(p.x)
print(p.y)

