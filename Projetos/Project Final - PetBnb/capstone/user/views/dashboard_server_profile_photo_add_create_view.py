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
from user.forms.server_profile_photo_model_form import ServerProfilePhotoModelForm


class DashboardServerProfilePhotoAddCreateView(CreateView):
    template_name = settings.BASE_DIR / 'user/templates/dashboard_server_profile_photo_add_create_view.html'
    form_class = ServerProfilePhotoModelForm
    success_url = reverse_lazy('dashboard_server_local_photos_list_view')

    @is_authenticated
    @has_profile_server
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    @is_authenticated
    @has_profile_client
    @has_profile_server
    def get_context_data(self, **kwargs):
        context = super(DashboardServerProfilePhotoAddCreateView, self).get_context_data(**kwargs)
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
        photo = form.save(commit=False)
        photo.user = self.request.user
        photo.save()
        self.add_local_photos(photo.pk)
        return super(DashboardServerProfilePhotoAddCreateView, self).form_valid(form, *args, **kwargs)

    def add_local_photos(self, pk):
        profile_server = self.request.user.profile_server.all()[0]
        __local_photos = str()
        get_local_photos = profile_server.get_local_photos
        if len(str(get_local_photos)) == 0:
            __local_photos = f"['{str(pk)}']"
            profile_server.local_photos = __local_photos
            profile_server.save()
        else:
            __local_photos = '['
            for i in profile_server.to_list(get_local_photos):
                __local_photos = __local_photos + f"'{i}',"
            __local_photos = __local_photos + f"'{pk}']"
            profile_server.local_photos = __local_photos
            profile_server.save()

