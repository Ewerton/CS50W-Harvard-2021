from django.conf import settings
from django.views.generic import (
    ListView,
    DeleteView,
    DetailView,
    CreateView,
    UpdateView,
    TemplateView
)

from availability.models.availability import Availability
from user.models.profile_server import ProfileServer
from photo.models.photo import Photo


class SearchDetailView(DetailView):
    template_name = settings.BASE_DIR / 'user/templates/search_detail_view.html'
    model = ProfileServer

    def get_context_data(self, **kwargs):
        context = super(SearchDetailView, self).get_context_data(**kwargs)
        profile_server = kwargs['object']
        context['viewing_its_own_page'] = False

        if self.request.user.is_authenticated:

            if (profile_server.user.id == self.request.user.id):
                context['viewing_its_own_page'] = True

            if len(self.request.user.profile_client.all()) >> 0:
                context['profile_client'] = self.request.user.profile_client.all()[0]

        if len(str(profile_server.local_photos)) >> 0:
            __local_photos = list()
            for i in profile_server.to_list(profile_server.local_photos):
                try:
                    __photo = Photo.objects.get(id=(int(i))).get_photo
                    __local_photos.append(__photo)
                except:
                    pass
            context['local_photos_list'] = __local_photos
        """
        
        context['availability_list'] = Availability.objects.filter(
            profile_server=profile_server
        )
        """
        return context
