from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DeleteView,
    DetailView,
    CreateView,
    UpdateView,
    TemplateView
)

from booking.models.booking import Booking
from utils.functions import is_authenticated
from utils.functions import has_profile_server
from utils.functions import has_profile_client
from user.forms.server_profile_availability_model_form import ServerProfileAvailabilityModelForm
from availability.models.availability import Availability
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class DashboardServerProfileAvailabilityAddCreateView(CreateView):
    template_name = settings.BASE_DIR / 'user/templates/dashboard_server_profile_availability_add_create_view.html'
    form_class = ServerProfileAvailabilityModelForm
    success_url = reverse_lazy('dashboard_server_availability_list_view')

    @is_authenticated
    @has_profile_server
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    @is_authenticated
    @has_profile_client
    @has_profile_server
    def get_context_data(self, **kwargs):
        context = super(DashboardServerProfileAvailabilityAddCreateView, self).get_context_data(**kwargs)
        # profile_client = self.request.user.profile_client.all()
        # if len(profile_client) >> 0:
        #     profile_client = profile_client[0]
        #     profile_client_booking = Booking.objects.filter(profile_client=profile_client, status=2).order_by('-id')
        #     context['notification_len'] = len(profile_client_booking)
        #     context['profile_client_notification'] = profile_client_booking[:3]

        # profile_server = self.request.user.profile_server.all()
        # if len(profile_server) >> 0:
        #     profile_server = profile_server[0]
        #     profile_server_booking = Booking.objects.filter(profile_server=profile_server, status=0).order_by('-id')
        #     context['notification_len'] += len(profile_server_booking)
        #     context['profile_server_notification'] = profile_server_booking[:3]
        #     context['profile_server'] = profile_server
        return context

    @is_authenticated
    @has_profile_server
    def form_valid(self, form, *args, **kwargs):
        profile_server = self.request.user.profile_server.all()[0]
        date = [str(a.date) for a in Availability.objects.filter(profile=profile_server)]
        availability = form.save(commit=False)
        availability.profile = profile_server
        if str(availability.date) in date:
            return HttpResponseRedirect(reverse_lazy('dashboard_server_availability_list_view'))
        availability.save()
        return super(DashboardServerProfileAvailabilityAddCreateView, self).form_valid(form, *args, **kwargs)
