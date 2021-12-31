from django.conf import settings
from django.views.generic import (
    ListView,
    DeleteView,
    DetailView,
    CreateView,
    UpdateView,
    TemplateView
)
from utils.functions import is_authenticated
from utils.functions import has_profile_client
from booking.models.booking import Booking
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from user.models.profile_server import ProfileServer


class DashboardClientBookingDetailView(DetailView):
    template_name = settings.BASE_DIR / 'user/templates/dashboard_client_booking_detail_view.html'
    model = Booking

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__pk = None

    @is_authenticated
    @has_profile_client
    def get(self, *args, **kwargs):
        if 'pk' in kwargs:
            try:
                pk = int(kwargs['pk'])
                booking = [b.id for b in self.request.user.profile_client.all()[0].booking.all()]
                if pk in booking:
                    self.__pk = pk
                    return super().get(self, *args, **kwargs)
                else:
                    return HttpResponseRedirect(reverse_lazy('dashboard_client_booking'))
            except ValueError:
                return HttpResponseRedirect(reverse_lazy('dashboard_client_booking'))
        else:
            return HttpResponseRedirect(reverse_lazy('dashboard_client_booking'))

    def get_context_data(self, **kwargs):
        context = super(DashboardClientBookingDetailView, self).get_context_data(**kwargs)
        # profile_client = self.request.user.profile_client.all()
        # if len(profile_client) >> 0:
        #     profile_client = profile_client[0]
        #     profile_client_booking = Booking.objects.filter(profile_client=profile_client, status=2).order_by('-id')
        #     context['notification_len'] = len(profile_client_booking)
        #     context['profile_client_notification'] = profile_client_booking[:3]
        #     context['profile_client'] = profile_client

        # profile_server = self.request.user.profile_server.all()
        # if len(profile_server) >> 0:
        #     profile_server = profile_server[0]
        #     profile_server_booking = Booking.objects.filter(profile_server=profile_server, status=0).order_by('-id')
        #     context['notification_len'] += len(profile_server_booking)
        #     context['profile_server_notification'] = profile_server_booking[:3]
        return context

    def get_object(self, queryset=None):
        booking = Booking.objects.get(id=self.__pk)
        if booking.status == 2:
            booking.status = 3
            booking.save()

        return booking
