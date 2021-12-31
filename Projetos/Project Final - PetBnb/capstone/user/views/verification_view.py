from django.views import View
from django.utils.http import urlsafe_base64_decode
from user.models.user import User
from user.utils.token_generator import TokenGenerator
from django.shortcuts import redirect
import logging


class VerificationView(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            __id = int(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=__id)

            if not TokenGenerator().check_token(user, token):
                return redirect('login')

            if user.is_active:
                return redirect('login')

            user.is_active = True
            user.save()

            return redirect('login')

        except Exception as err:
            logging.exception(err)
            pass

        return redirect('login')
