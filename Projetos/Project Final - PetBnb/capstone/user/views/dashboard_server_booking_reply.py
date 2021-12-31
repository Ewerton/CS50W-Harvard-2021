from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from utils.functions import is_authenticated
from utils.functions import has_profile_server
from booking.models.booking import Booking
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


@is_authenticated
@has_profile_server
def dashboard_server_booking_reply(request, **kwargs):
    if request.method == 'GET':
        template = loader.get_template(settings.BASE_DIR / 'user/templates/dashboard_server_booking_reply.html')
        pk = int(kwargs['pk'])
        ids = [int(i.id) for i in request.user.profile_server.all()[0].booking.all()]
        if pk not in ids:
            return HttpResponseRedirect(reverse_lazy('dashboard_server_booking_list_view'))

        booking = Booking.objects.get(id=pk)
        if booking.status == 0:
            booking.status = 1
            booking.save()

        context = {
            'object': booking
        }

        # profile_client = request.user.profile_client.all()
        # if len(profile_client) >> 0:
        #     profile_client = profile_client[0]
        #     profile_client_booking = Booking.objects.filter(profile_client=profile_client, status=2).order_by('-id')
        #     context['notification_len'] = len(profile_client_booking)
        #     context['profile_client_notification'] = profile_client_booking[:3]
        #     context['profile_client'] = profile_client

        # profile_server = request.user.profile_server.all()
        # if len(profile_server) >> 0:
        #     profile_server = profile_server[0]
        #     profile_server_booking = Booking.objects.filter(profile_server=profile_server, status=0).order_by('-id')
        #     context['notification_len'] += len(profile_server_booking)
        #     context['profile_server_notification'] = profile_server_booking[:3]
        #     context['profile_server'] = profile_server

        return HttpResponse(template.render(context, request), content_type='text/html', charset='utf-8')

    elif request.method == 'POST':
        pk = int(kwargs['pk'])
        ids = [int(i.id) for i in request.user.profile_server.all()[0].booking.all()]
        if pk not in ids:
            return HttpResponseRedirect(reverse_lazy('dashboard_server_booking_list_view'))

        items = dict(request.POST.items())
        if ('confirmed' and 'decision') in items:
            confirmed = int(items.get('confirmed'))
            decision = str(items.get('decision'))
            if confirmed == 1 or confirmed == 2:
                booking = Booking.objects.get(id=pk)
                if booking.status == 1:
                    booking.confirmed = confirmed
                    booking.decision = decision
                    booking.status = 2
                    booking.save()
                    return HttpResponseRedirect(reverse_lazy('dashboard_server_booking_reply',  kwargs={'pk': pk}))
                else:
                    return HttpResponseRedirect(reverse_lazy('dashboard_server_booking_list_view'))
            else:
                return HttpResponseRedirect(reverse_lazy('dashboard_server_booking_list_view'))
        else:
            return HttpResponseRedirect(reverse_lazy('dashboard_server_booking_list_view'))
