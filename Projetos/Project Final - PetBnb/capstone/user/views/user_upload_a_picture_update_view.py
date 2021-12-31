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
from user.forms.user_update_form import UserUpdateForm
from user.models.user import User


class UserUploadAPictureUpdateView(UpdateView):
    template_name = settings.BASE_DIR / 'user/templates/user_upload_a_picture_update_view.html'
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('dashboard_client_profile_detail_view')

    @is_authenticated
    @has_profile_client
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    @is_authenticated
    @has_profile_client
    def get_context_data(self, **kwargs):
        context = super(UserUploadAPictureUpdateView, self).get_context_data(**kwargs)
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
