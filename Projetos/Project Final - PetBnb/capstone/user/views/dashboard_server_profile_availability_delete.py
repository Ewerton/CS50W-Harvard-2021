from utils.functions import is_authenticated
from utils.functions import has_profile_server
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from availability.models.availability import Availability


@is_authenticated
@has_profile_server
def dashboard_server_profile_availability_delete(request, *args, **kwargs):
    if 'pk' in kwargs:
        try:
            pk = int(kwargs['pk'])
            profile_server = request.user.profile_server.all()[0]
            availability = [a.id for a in Availability.objects.filter(profile=profile_server)]
            if pk in availability:
                Availability.objects.get(id=pk).delete()
                return HttpResponseRedirect(reverse_lazy('dashboard_server_availability_list_view'))
            else:
                return HttpResponseRedirect(reverse_lazy('dashboard_server_availability_list_view'))
        except ValueError:
            return HttpResponseRedirect(reverse_lazy('dashboard_server_availability_list_view'))
    else:
        return HttpResponseRedirect(reverse_lazy('dashboard_server_availability_list_view'))
