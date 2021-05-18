from django import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Se criar essa variável global todos os usuários verão a mesma lista de tasks
# o ideal é salvar na Session
# tasks = []

# Cria um form html e passa ele para o template html para ser renderizado

# mapeia os objetos do html form para um objeto
class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    priority = forms.IntegerField(label="priority", min_value=1, max_value=10)

# Create your views here.


def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = [] # se não existir uma lista de tasks, crio uma

    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })


def add(request):
    # se o request for POST
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            # Obtem a task que o usuário postou no form
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]  # adiciona na lista de tasks
            return HttpResponseRedirect(reverse("tasks:index")) # passo o nome da url e o Django fas "engenharia reversa pra descobrir qual é a URL"
        else:
            return render(request, "tasks/add.html", {
                "form":  form  # retorna o mesmo form que ele submeteu para que ele possa ver os erros que ocorreram
            })

    # se o o request for GET
    return render(request, "tasks/add.html", {
        "form": NewTaskForm()  # Passa o form criado para o template HTML
    })
