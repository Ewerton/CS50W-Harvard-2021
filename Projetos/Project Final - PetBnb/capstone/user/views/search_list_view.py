from datetime import datetime
from django.conf import settings
from django.views.generic import (
    ListView,
    DeleteView,
    DetailView,
    CreateView,
    UpdateView,
    TemplateView
)
from urllib.parse import parse_qs
from availability.models.availability import Availability
from user.models.profile_server import ProfileServer


class SearchListView(ListView):
    template_name = settings.BASE_DIR / 'user/templates/search_list_view.html'
    model = ProfileServer
    paginate_by = 9

    def __init__(self, *args, **kwargs):
        super(SearchListView, self).__init__(*args, **kwargs)
        self.__type_of_pet = str()
        self.__check_in = str()
        self.__check_out = str()

    def get(self, *args, **kwargs):
        __args = args[0].__dict__.copy()
        query = __args['environ']['QUERY_STRING']
        params = parse_qs(query)

        if 'type_of_pet' in params:
            try:
                self.__type_of_pet = int(params['type_of_pet'][0])
            except ValueError:
                pass

        if 'check_in' in params:
            self.__check_in = params['check_in'][0]

        if 'check_out' in params:
            self.__check_out = params['check_out'][0]

        return super().get(self, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SearchListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            if len(self.request.user.profile_client.all()) >> 0:
                context['profile_client'] = self.request.user.profile_client.all()[0]
        return context

    def get_queryset(self):
        if isinstance(self.__type_of_pet, int) > 0 and len(self.__check_in) > 0 and len(self.__check_out) > 0:
            __filter = Availability.objects.filter(date__range=[self.__check_in, self.__check_out]).filter(
                profile__pet_type__contains=f"'{self.__type_of_pet}'"
            )
            profile_list = list()
            if not self.request.user.is_authenticated:
                [profile_list.append(profile.id) for profile in [availability.profile for availability in __filter] if profile.id not in profile_list]
            else:
                if len(self.request.user.profile_server.all()) == 0:
                    [profile_list.append(profile.id) for profile in [availability.profile for availability in __filter] if profile.id not in profile_list]
                else:
                    [profile_list.append(profile.id) for profile in [availability.profile for availability in __filter] if profile.id not in profile_list and profile != self.request.user.profile_server.all()[0]]
            return ProfileServer.objects.filter(id__in=profile_list)

        elif isinstance(self.__type_of_pet, int):
            __filter = Availability.objects.filter(
                profile__pet_type__contains=f"'{self.__type_of_pet}'"
            )
            profile_list = list()
            if not self.request.user.is_authenticated:
                [profile_list.append(profile.id) for profile in [availability.profile for availability in __filter] if profile.id not in profile_list]
            else:
                if len(self.request.user.profile_server.all()) == 0:
                    [profile_list.append(profile.id) for profile in [availability.profile for availability in __filter] if profile.id not in profile_list]
                else:
                    [profile_list.append(profile.id) for profile in [availability.profile for availability in __filter] if profile.id not in profile_list and profile != self.request.user.profile_server.all()[0]]
            return ProfileServer.objects.filter(id__in=profile_list)
        else:
            return ProfileServer.objects.none()
