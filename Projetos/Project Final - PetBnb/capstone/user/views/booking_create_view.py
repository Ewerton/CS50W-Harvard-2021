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
from utils.functions import is_authenticated
from utils.functions import has_profile_client
from user.forms.booking_model_form import BookingModelForm
from availability.models.availability import Availability
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from booking.models.booking import Booking


class BookingCreateView(CreateView):
    template_name = settings.BASE_DIR / 'user/templates/booking_create_view.html'
    form_class = BookingModelForm
    success_url = reverse_lazy('home_template_view')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__availability = None
        self.__profile_server = None
        self.__user = None
        self.__pk = None
        self.__profile_client = None

    @is_authenticated
    @has_profile_client
    def get(self, *args, **kwargs):
        availability_pk = int(kwargs['pk'])
        self.__availability = Availability.objects.get(id=availability_pk)
        self.__profile_server = self.__availability.profile
        self.__user = self.__profile_server.user
        if self.__user == self.request.user:
            return HttpResponseRedirect(reverse_lazy('home_template_view'))
        return super().get(self, *args, **kwargs)

    @is_authenticated
    @has_profile_client
    def post(self, request, *args, **kwargs):
        self.__pk = int(kwargs['pk'])
        self.__availability = Availability.objects.get(id=self.__pk)
        self.__profile_server = self.__availability.profile
        self.__profile_client = self.request.user.profile_client.all()[0]
        return super().post(self, request, *args, **kwargs)

    @is_authenticated
    @has_profile_client
    def get_context_data(self, **kwargs):
        context = super(BookingCreateView, self).get_context_data(**kwargs)
        context['profile_client'] = self.request.user.profile_client.all()[0]
        context['profile_server'] = self.__profile_server
        context['availability'] = self.__availability

        return context

    @is_authenticated
    @has_profile_client
    def form_valid(self, form, *args, **kwargs):
        pet_photo_ids = [int(form.data[i]) for i in form.data.keys() if str(i).startswith('pet_photo_')]
        pet_description = form.data['pet_description']
        if len(pet_photo_ids) == 0:
            return HttpResponseRedirect(reverse_lazy('booking_create_view', kwargs={'pk': self.__pk}))

        if len(str(pet_description)) == 0:
            return HttpResponseRedirect(reverse_lazy('booking_create_view', kwargs={'pk': self.__pk}))

        __pet_photo = '['
        for i in pet_photo_ids[0:len(pet_photo_ids)-1]:
            __pet_photo = __pet_photo + f"'{i}',"
        __pet_photo = __pet_photo + f"'{pet_photo_ids[-1]}']"

        booking = form.save(commit=False)
        booking.profile_client = self.__profile_client
        booking.profile_server = self.__profile_server
        booking.pet_photo = __pet_photo
        booking.pet_description = pet_description
        booking.date_of_interest = self.__availability.date
        """
        booking_list = [str(a.date_of_interest) for a in Booking.objects.filter(profile_client=self.__profile_client,
                                                                                profile_server=self.__profile_server)]
        if str(self.__availability.date) in booking_list:
            return HttpResponseRedirect(reverse_lazy('search_detail_view', kwargs={'pk': self.__profile_server.id}))
        """
        booking.confirmed = 0
        booking.status = 0
        booking.save()
        return HttpResponseRedirect(reverse_lazy('search_detail_view', kwargs={'pk': self.__profile_server.id}))
