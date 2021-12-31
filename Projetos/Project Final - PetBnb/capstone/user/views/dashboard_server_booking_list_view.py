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
from utils.functions import has_profile_server
from booking.models.booking import Booking


class DashboardServerBookingListView(ListView):
    template_name = settings.BASE_DIR / 'user/templates/dashboard_server_booking_list_view.html'
    model = Booking
    paginate_by = 9

    @is_authenticated
    @has_profile_server
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.request.session['last_visited_profile_type'] = 'server'
        context = super(DashboardServerBookingListView, self).get_context_data(**kwargs)
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

    def get_queryset(self):
        return Booking.objects.filter(profile_server=self.request.user.profile_server.all()[0])
