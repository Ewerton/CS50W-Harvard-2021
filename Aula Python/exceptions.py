import sys

try:
    x = int(input("x: "))
    y = int(input("y: "))
except ValueError:
    print("Error: Invalid input.")
    sys.exit(1)
    
try:
    result = x / y  # pode ocorrer ZeroDivisionError: division by zero
except ZeroDivisionError:
    print("Error: Cannot divide by 0.")
    sys.exit(1)  # fecha o programa informando ao S.O que deu erro

print(f"{x} / {y} equals: {result}")
