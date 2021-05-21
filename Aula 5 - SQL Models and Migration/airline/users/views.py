from django.shortcuts import render
from django.http import HttpResponseRedirect 
from django.urls import reverse

# oferece funções prntas para login, logout e autenticação
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render (request, "users/user.html")
    
def login_view(request):
    if request.method =="POST":
        # obtem nome e password do form de loginn postado
        usernameReceived = request.POST["username"]
        passwordReceived = request.POST["password"]

        #tenta autenticar o usuário
        user = authenticate(request, username=usernameReceived, password=passwordReceived)
        if (user is not None):
            login(request, user) # se conseguiu authenticar, loga o usuário.
            return HttpResponseRedirect(reverse("index")) #redireciona para a pagina principal
        else:
            return render(request, "users/login.html", {
                "message": "Invalid credentials."
            })

    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {
        "message": "Logged Out."
    })