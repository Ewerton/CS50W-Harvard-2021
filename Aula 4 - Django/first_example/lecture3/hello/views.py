from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
# Para criar uma view vc define uma function que recebe um request como parametro
# def index(request):
#     return HttpResponse("Hello World")

def index(request):
    return render(request, "hello/index.html") 

# def ewerton(request):
#     return HttpResponse("Hello Ewerton")

# def taylise(request):
#     return HttpResponse("Hello Taylise")

# def marwin(request):
#     return HttpResponse("Hello Marwin")

# Ao invés disso, posso criar uma função greet e usar url patterns para rotear para a função correta
def greet(request, name):
    return HttpResponse(f"Hello, {name.capitalize()}!")

# Ou, melhor ainda, posso usar uma pagina HTML como template 
def greet(request, name):
    return render(request, "hello/greet.html", {
        # aqui vai o contexto, ou todas as variáveis que quero passar para o HTML com dictionary.
        "name": name.capitalize()
    })