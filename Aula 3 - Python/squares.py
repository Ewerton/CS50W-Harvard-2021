# importa do módulo "functions" que foi definido em outro arquivo a função "square"
from functions import square
#import functions

for i in range(10):
    print(f"The square of {i} is {square(i)}") #print(f"The square of {i} is {square(i)}")

#outra forma
#import functions

#for i in range(10):
#    print(f"The square of {i} is {functions.square(i)}") 
