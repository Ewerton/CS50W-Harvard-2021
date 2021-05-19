from django.contrib import admin

from .models import Flight, Airport, Passenger

# Edita como a lista de flights vai ser exibida no admin.
# Mais detalhes das opções disponiveis, ver documentação do Django
class FlightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "duration") # determina quais colunas apareceção na grid que lista os voos

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",) # Habilita duas caixas de seleção util quando se tem many to many

# Register your models here.
admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger, PassengerAdmin)