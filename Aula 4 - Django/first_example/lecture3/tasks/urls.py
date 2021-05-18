from django.urls import path
from . import views  # Do diretorio atual (.) importe o arquivo views.py

#app_name é importante aqui porque no app newyear também existe uma rota com o nome de index, então, 
# quando tentamos # linkar a url index do app tasks (<a href="{% url 'index' %}"></a>), o django vai 
# procurar no projeto todo vai achar mais de um o que vai resultar em um conflito de nomes
# então, colocamos o app name e usamos a seguinte para linkar uma pagina no html (<a href="{% url 'tasks:index' %}"></a>)
app_name = "tasks"
urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add")
]