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
from utils.functions import has_profile_client
from utils.functions import has_profile_server
from user.forms.server_profile_model_form import ServerProfileModelForm
from user.models.profile_server import ProfileServer


class DashboardServerProfileUpdateView(UpdateView):
    template_name = settings.BASE_DIR / 'user/templates/dashboard_server_profile_update_view.html'
    model = ProfileServer
    form_class = ServerProfileModelForm
    success_url = reverse_lazy('dashboard_server_profile_detail_view')

    @is_authenticated
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    @is_authenticated
    @has_profile_client
    @has_profile_server
    def get_context_data(self, **kwargs):
        context = super(DashboardServerProfileUpdateView, self).get_context_data(**kwargs)
        # profile_client = self.request.user.profile_client.all()
        # if len(profile_client) >> 0:
        #     profile_client = profile_client[0]
        #     profile_client_booking = Booking.objects.filter(profile_client=profile_client, status=2).order_by('-id')
        #     context['notification_len'] = len(profile_client_booking)
        #     context['profile_client_notification'] = profile_client_booking[:3]

        profile_server = self.request.user.profile_server.all()
        if len(profile_server) >> 0:
            profile_server = profile_server[0]
        #     profile_server_booking = Booking.objects.filter(profile_server=profile_server, status=0).order_by('-id')
        #     context['notification_len'] += len(profile_server_booking)
        #     context['profile_server_notification'] = profile_server_booking[:3]
            context['profile_server'] = profile_server
            context['pet_type_ids'] = profile_server.to_list(profile_server.pet_type)

        return context

    def get_object(self, queryset=None):
        return self.request.user.profile_server.all()[0]

    @is_authenticated
    def form_valid(self, form, *args, **kwargs):
        profile_client = form.save(commit=False)
        profile_client.user = self.request.user
        profile_client.save()
        return super(DashboardServerProfileUpdateView, self).form_valid(form, *args, **kwargs)
