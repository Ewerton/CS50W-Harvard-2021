from django.conf import settings
from django.views.generic import CreateView
from user.forms.user_create_form import UserCreateForm
from django.urls import reverse_lazy


class UserCreateView(CreateView):
    template_name = settings.BASE_DIR / 'user/templates/auth/register.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
