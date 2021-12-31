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
from photo.models.photo import Photo
from availability.models.availability import Availability
from booking.models.booking import Booking


class DashboardClientPhotoOfMyPetListView(ListView):
    template_name = settings.BASE_DIR / 'user/templates/dashboard_client_photo_of_my_pet_list_view.html'
    model = Photo
    paginate_by = 9

    @is_authenticated
    @has_profile_client
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardClientPhotoOfMyPetListView, self).get_context_data(**kwargs)
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

    def get_queryset(self):
        profile_client = self.request.user.profile_client.all()[0]
        if len(str(profile_client.get_pet_photo)) >> 0:
            print(profile_client.to_list(profile_client.pet_photo))
            pet_photo_list = [int(i) for i in profile_client.to_list(profile_client.pet_photo)]
            return Photo.objects.filter(id__in=pet_photo_list)
        return Photo.objects.none()
