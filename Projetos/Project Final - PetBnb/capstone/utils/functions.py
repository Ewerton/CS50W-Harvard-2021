import os
from time import strftime
from functools import wraps
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


def upload_to_path(instance, filename):
    ext = filename.split('.')[-1]

    filename = "%s_%s_%s_%s_%s_%s.%s" % (
        strftime('%y'),
        strftime('%m'),
        strftime('%d'),
        strftime('%H'),
        strftime('%M'),
        strftime('%S'),
        ext
    )
    return os.path.join('uploads', filename)


def is_authenticated(fn):
    """
    Only allow the user to access the panel after logging in
    """

    @wraps(fn)
    def get(self, *args, **kwargs):
        try:
            if not self.request.user.is_authenticated:
                return HttpResponseRedirect(reverse_lazy('login'))
        except AttributeError:
            if not self.user.is_authenticated:
                return HttpResponseRedirect(reverse_lazy('login'))
        return fn(self, *args, **kwargs)

    return get


def has_profile_client(fn):
    """
    Only allows access to the panel after completing the profile.
    """

    @wraps(fn)
    def get(self, *args, **kwargs):
        try:
            profile_client = self.request.user.profile_client.all()
            if len(profile_client) == 0:
                return HttpResponseRedirect(reverse_lazy('dashboard_client_profile_create_view'))
        except AttributeError:
            profile_client = self.user.profile_client.all()
            if len(profile_client) == 0:
                return HttpResponseRedirect(reverse_lazy('dashboard_client_profile_create_view'))
        return fn(self, *args, **kwargs)

    return get


def not_has_profile_client(fn):
    """
    Does not allow the user to access the profile registration form more than once
    """

    @wraps(fn)
    def get(self, *args, **kwargs):
        try:
            profile_client = self.request.user.profile_client.all()
            if len(profile_client) >> 0:
                return HttpResponseRedirect(reverse_lazy('dashboard_client_list_view'))
        except AttributeError:
            profile_client = self.user.profile_client.all()
            if len(profile_client) >> 0:
                return HttpResponseRedirect(reverse_lazy('dashboard_client_list_view'))
        return fn(self, *args, **kwargs)

    return get


def has_profile_server(fn):
    """
    Only allows access to the panel after completing the profile.
    """

    @wraps(fn)
    def get(self, *args, **kwargs):
        try:
            profile_server = self.request.user.profile_server.all()
            if len(profile_server) == 0:
                return HttpResponseRedirect(reverse_lazy('dashboard_server_profile_create_view'))
        except AttributeError:
            profile_server = self.user.profile_server.all()
            if len(profile_server) == 0:
                return HttpResponseRedirect(reverse_lazy('dashboard_server_profile_create_view'))
        return fn(self, *args, **kwargs)

    return get


def not_has_profile_server(fn):
    """
    Does not allow the user to access the profile registration form more than once
    """

    @wraps(fn)
    def get(self, *args, **kwargs):
        try:
            profile_server = self.request.user.profile_server.all()
            if len(profile_server) >> 0:
                return HttpResponseRedirect(reverse_lazy('dashboard_server_list_view'))
        except AttributeError:
            profile_server = self.user.profile_server.all()
            if len(profile_server) >> 0:
                return HttpResponseRedirect(reverse_lazy('dashboard_server_list_view'))
        return fn(self, *args, **kwargs)

    return get
