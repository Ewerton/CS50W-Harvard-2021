from django.conf import settings
from django.views.generic import (
    ListView,
    DeleteView,
    DetailView,
    CreateView,
    UpdateView,
    TemplateView
)
from pet_type.models.pet_type import PetType


class HomeTemplateView(TemplateView):
    template_name = settings.BASE_DIR / 'user/templates/home_template_view.html'

    def get_context_data(self, **kwargs):
        context = super(HomeTemplateView, self).get_context_data(**kwargs)
        context['pet_type'] = PetType.objects.all()
        if self.request.user.is_authenticated:
            if len(self.request.user.profile_client.all()) >> 0:
                context['profile_client'] = self.request.user.profile_client.all()[0]
        return context

