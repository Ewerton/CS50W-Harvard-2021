from django.http import HttpResponse
from django.template import loader
from django.conf import settings

from booking.models.booking import Booking
from utils.functions import is_authenticated
from photo.models.photo import Photo
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


@is_authenticated
def dashboard_server_profile_photo_delete(request):
    template = loader.get_template(settings.BASE_DIR / 'user/templates/dashboard_server_profile_photo_delete.html')
    context = {}
    if request.method == 'GET':
        context['profile_client'] = request.user.profile_client.all()[0]
        profile_server = request.user.profile_server.all()
        if len(profile_server) >> 0:
            # returns the first user profile_server
            profile_server = profile_server[0]
            context['profile_server'] = profile_server
            if len(str(profile_server.local_photos)) >> 0:

                profile_client = request.user.profile_client.all()
                if len(profile_client) >> 0:
                    profile_client = profile_client[0]
                    profile_client_booking = Booking.objects.filter(profile_client=profile_client, status=2).order_by(
                        '-id')
                    context['notification_len'] = len(profile_client_booking)
                    context['profile_client_notification'] = profile_client_booking[:3]

                    profile_server_booking = Booking.objects.filter(profile_server=profile_server, status=0).order_by(
                        '-id')
                    context['notification_len'] += len(profile_server_booking)
                    context['profile_server_notification'] = profile_server_booking[:3]

                __local_photos = list()
                for i in profile_server.to_list(profile_server.local_photos):
                    try:
                        __photo = Photo.objects.get(id=(int(i))).get_photo
                        __local_photos.append((i, __photo))
                    except:
                        pass
                context['local_photos_list'] = __local_photos
            else:
                return HttpResponseRedirect(reverse_lazy('dashboard_server_profile_photo_add_create_view'))
        else:
            return HttpResponseRedirect(reverse_lazy('dashboard_server_profile_create_view'))

        return HttpResponse(template.render(context, request), content_type='text/html', charset='utf-8')
    elif request.method == 'POST':

        profile_server = request.user.profile_server.all()
        if len(profile_server) >> 0:
            profile_server = profile_server[0]
            context['profile_server'] = profile_server
            if len(str(profile_server.local_photos)) >> 0:
                local_photos_list = profile_server.to_list(profile_server.local_photos)

                local_photos_delete_list = list()
                for _, value in request.POST.items():
                    if value in local_photos_list:
                        local_photos_delete_list.append(value)

                local_photos_list = [i for i in local_photos_list if i not in local_photos_delete_list]

                if len(local_photos_list) == 0:
                    profile_server.local_photos = ''
                else:
                    profile_server.local_photos = local_photos_list
                profile_server.save()

                for i in local_photos_delete_list:
                    try:
                        Photo.objects.get(id=int(i)).delete()
                    except:
                        pass
                return HttpResponseRedirect(reverse_lazy('dashboard_server_local_photos_list_view'))
            else:
                return HttpResponseRedirect(reverse_lazy('dashboard_server_profile_photo_add_create_view'))
        else:
            return HttpResponseRedirect(reverse_lazy('dashboard_server_profile_create_view'))
