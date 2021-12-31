from django.http.response import JsonResponse
from booking.models.review import Review
from utils.functions import is_authenticated
from utils.functions import has_profile_client
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from booking.models.booking import Booking
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.template.context import Context
from django.shortcuts import render
from user.templatetags import petbnb_extras
from user.models.profile_server import ProfileServer

#@is_authenticated
@is_authenticated
@csrf_exempt
def booking_review(request, **kwargs):
        
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    if request.user.id is None:
        return JsonResponse({"error": "No user logged in."}, status=400)

    if not request.is_ajax() and request.method == 'POST': 
        return JsonResponse({"error": "AJAX request required."}, status=400)

    if request.is_ajax() and request.method == 'POST':
        if request.POST.get('userReviewing') is None:
            return JsonResponse({"error": "User Reviewing is required."}, status=400)

        if request.POST.get('userReviewed') is None:
            return JsonResponse({"error": "User Reviewed is required."}, status=400)
        
        if request.POST.get('reviewText') is None:
            return JsonResponse({"error": "Review Text is required."}, status=400)
        
        if request.POST.get('bookingId') is None:
            return JsonResponse({"error": "Booking Id is required."}, status=400)
        
        if request.POST.get('number_of_stars') is None:
            return JsonResponse({"error": "Number of stars is required."}, status=400)

        userReviewing = request.POST.get('userReviewing')
        userReviewed = request.POST.get('userReviewed')
        reviewText = request.POST.get('reviewText')
        bookingId = request.POST.get('bookingId')
        number_of_stars = request.POST.get('number_of_stars')

        new_review = Review.objects.create(date = timezone.now(), 
                                            comment = reviewText,  
                                            rating=number_of_stars, 
                                            profile_client_author_id = userReviewing,
                                            profile_server_reviewed_id = userReviewed, 
                                            booking_id =bookingId)
        new_review.save()
        return JsonResponse({"success": "Review saved."}, status=200)

@is_authenticated
@csrf_exempt
def booking_review_delete(request, **kwargs):
    if request.method != "DELETE":
        return JsonResponse({"error": "DELETE request required."}, status=400)
    
    if request.user.id is None:
        return JsonResponse({"error": "No user logged in."}, status=400)

    if not request.is_ajax() and request.method == 'DELETE': 
        return JsonResponse({"error": "AJAX request required."}, status=400)

    if request.is_ajax() and request.method == 'DELETE':
        reviewId = kwargs["pk"]
        Review.objects.get(pk=reviewId).delete()
        return JsonResponse({"success": "Succesfully deleted."}, status=200)


# renders the reviews list template
@login_required
def booking_review_list(request, **kwargs):
    context = Context({'request': request})
    profileserver_viewing = ProfileServer.objects.get(id=int(kwargs['pk']))
    return render(request, 'templates/reviews_list.html', petbnb_extras.reviews_list_template(context, profileserver_viewing) )