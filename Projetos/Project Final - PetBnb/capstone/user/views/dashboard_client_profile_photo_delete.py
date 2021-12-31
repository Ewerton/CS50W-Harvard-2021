from utils.functions import is_authenticated
from utils.functions import has_profile_client
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from photo.models.photo import Photo


@is_authenticated
@has_profile_client
def dashboard_client_profile_photo_delete(request, *args, **kwargs):
    if 'pk' in kwargs:
        try:
            pk = int(kwargs['pk'])
            profile_client = request.user.profile_client.all()[0]
            pet_photo_list = [int(i) for i in profile_client.to_list(profile_client.pet_photo)]
            if pk in pet_photo_list:
                Photo.objects.get(id=pk).delete()
                pet_photo_list.remove(pk)
                if len(pet_photo_list) == 0:
                    profile_client.pet_photo = ''
                else:
                    profile_client.pet_photo = pet_photo_list
                profile_client.save()
                return HttpResponseRedirect(reverse_lazy('dashboard_client_photo_of_my_pet_list_view'))
            else:
                return HttpResponseRedirect(reverse_lazy('dashboard_client_photo_of_my_pet_list_view'))
        except ValueError:
            return HttpResponseRedirect(reverse_lazy('dashboard_client_photo_of_my_pet_list_view'))
    else:
        return HttpResponseRedirect(reverse_lazy('dashboard_client_photo_of_my_pet_list_view'))
