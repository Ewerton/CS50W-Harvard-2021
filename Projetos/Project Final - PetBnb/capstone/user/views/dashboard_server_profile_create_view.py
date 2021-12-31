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
from utils.functions import not_has_profile_server
from utils.functions import has_profile_client
from user.forms.server_profile_model_form import ServerProfileModelForm


class DashboardServerProfileCreateView(CreateView):
    template_name = settings.BASE_DIR / 'user/templates/dashboard_server_profile_create_view.html'
    form_class = ServerProfileModelForm
    success_url = reverse_lazy('dashboard_server_booking_list_view')

    @is_authenticated
    @not_has_profile_server
    def get(self, *args, **kwargs):
        return super().get(self, *args, **kwargs)

    @is_authenticated
    @has_profile_client
    def get_context_data(self, **kwargs):
        context = super(DashboardServerProfileCreateView, self).get_context_data(**kwargs)
        context['profile_client'] = self.request.user.profile_client.all()[0]
        return context

    @is_authenticated
    @not_has_profile_server
    def form_valid(self, form, *args, **kwargs):
        profile_client = form.save(commit=False)
        profile_client.user = self.request.user
        profile_client.save()
        return super(DashboardServerProfileCreateView, self).form_valid(form, *args, **kwargs)
