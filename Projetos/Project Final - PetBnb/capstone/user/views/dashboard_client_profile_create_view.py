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
from utils.functions import not_has_profile_client
from user.forms.client_profile_model_form import ClientProfileModelForm


class DashboardClientProfileCreateView(CreateView):
    template_name = settings.BASE_DIR / 'user/templates/dashboard_client_profile_create_view.html'
    form_class = ClientProfileModelForm
    success_url = reverse_lazy('dashboard_client_booking_list_view')

    @is_authenticated
    @not_has_profile_client
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    @is_authenticated
    @not_has_profile_client
    def form_valid(self, form, *args, **kwargs):
        profile_client = form.save(commit=False)
        profile_client.user = self.request.user
        profile_client.save()
        return super(DashboardClientProfileCreateView, self).form_valid(form, *args, **kwargs)
