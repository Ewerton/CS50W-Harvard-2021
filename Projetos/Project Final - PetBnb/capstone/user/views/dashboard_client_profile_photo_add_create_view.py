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
from user.forms.client_profile_photo_model_form import ClientProfilePhotoModelForm


class DashboardClientProfilePhotoAddCreateView(CreateView):
    template_name = settings.BASE_DIR / 'user/templates/dashboard_client_profile_photo_add_create_view.html'
    form_class = ClientProfilePhotoModelForm
    success_url = reverse_lazy('dashboard_client_photo_of_my_pet_list_view')

    @is_authenticated
    @has_profile_client
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    @is_authenticated
    @has_profile_client
    def get_context_data(self, **kwargs):
        context = super(DashboardClientProfilePhotoAddCreateView, self).get_context_data(**kwargs)
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

    @is_authenticated
    @has_profile_client
    def form_valid(self, form, *args, **kwargs):
        photo = form.save(commit=False)
        photo.user = self.request.user
        photo.save()
        self.add_pet_photo(photo.pk)
        return super(DashboardClientProfilePhotoAddCreateView, self).form_valid(form, *args, **kwargs)

    def add_pet_photo(self, pk):
        profile_client = self.request.user.profile_client.all()[0]
        __pet_photo = str()
        get_pet_photo = profile_client.get_pet_photo
        if len(str(get_pet_photo)) == 0:
            __pet_photo = f"['{str(pk)}']"
            profile_client.pet_photo = __pet_photo
            profile_client.save()
        else:
            __pet_photo = '['
            for i in profile_client.to_list(get_pet_photo):
                __pet_photo = __pet_photo + f"'{i}',"
            __pet_photo = __pet_photo + f"'{pk}']"
            profile_client.pet_photo = __pet_photo
            profile_client.save()

