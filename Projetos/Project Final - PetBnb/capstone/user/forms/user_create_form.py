from django import forms
from django.contrib.auth.forms import UserCreationForm
from user.models.user import User
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes
from user.utils.token_generator import TokenGenerator
from django.template import loader
from django.forms.widgets import MediaDefiningClass


class UserCreateForm(UserCreationForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta(metaclass=MediaDefiningClass):
        needs_multipart_form = False
        model = User
        fields = ('email', 'photo')
        labels = {'email': 'E-mail'}

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'multiple': False}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            self.send_email(user)
        return user

    @staticmethod
    def send_email(user) -> None:
        subject = _('Activate your account')
        context = {
            'user': user,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': TokenGenerator().make_token(user),
        }
        email_template_name = settings.BASE_DIR / 'user/templates/auth/activate_email.html',
        from_email = 'no-reply@example.com'
        body = loader.render_to_string(email_template_name, context)
        email_message = EmailMultiAlternatives(subject, body, from_email, [user.get_email])
        email_message.send(fail_silently=False)
