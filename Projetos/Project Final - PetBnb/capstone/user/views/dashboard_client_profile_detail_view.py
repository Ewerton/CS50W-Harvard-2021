from django.conf import settings
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
from user.models.profile_client import ProfileClient


class DashboardClientProfileDetailView(DetailView):
    template_name = settings.BASE_DIR / 'user/templates/dashboard_client_profile_detail_view.html'
    model = ProfileClient

    @is_authenticated
    @has_profile_client
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardClientProfileDetailView, self).get_context_data(**kwargs)
        profile_client = self.request.user.profile_client.all()
        if len(profile_client) >> 0:
            profile_client = profile_client[0]
            context['profile_client'] = profile_client
        return context

    def get_object(self, queryset=None):
        return self.request.user.profile_client.all()[0]
