from utils.functions import is_authenticated
from utils.functions import has_profile_client
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from booking.models.booking import Booking


@is_authenticated
@has_profile_client
def booking_cancel(request, **kwargs):
    if request.method == 'GET':
        booking = Booking.objects.get(id=int(kwargs['pk']))
        booking.confirmed = False
        booking.save()
        return HttpResponseRedirect(reverse_lazy('dashboard_client_list_view'))
    else:
        return HttpResponseRedirect(reverse_lazy('dashboard_client_list_view'))
