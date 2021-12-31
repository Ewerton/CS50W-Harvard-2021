from booking.models.ReviewResult import ReviewResult
from booking.models.reviewreply import ReviewReply
from booking.models.review import Review
from booking.models.booking import Booking
from django import template
from user.models import User
from user.models import profile_client
from django.db.models import Q
from datetime import datetime, timedelta

register = template.Library()

@register.inclusion_tag('templates/navbar.html', takes_context=True)
def navbar_template(context):
    request = get_request_from_context(context)
    current_user = get_current_user(request)
    is_dashboard = 'dashboard' in request.path
    #is_viewing_as_client = '/client/' in request.path
    is_home = request.path == '/'
    notification_len = 0
    #notification_items = []
    profile_client_notification_items = []
    profile_server_notification_items = []
    current_profile = None
    current_profile_name = ""
    profile_client = None
    profile_server = None

    if (not request.user.is_anonymous):
        if (request.user.profile_client != None):
            profile_client = request.user.profile_client.all()
            if len(profile_client) >> 0:
                profile_client = profile_client[0]
                profile_client_booking = Booking.objects.filter(profile_client=profile_client, status=2).order_by('-id')
                #profile_client_booking = list(Booking.objects.filter(profile_client=profile_client).order_by('-id'))
                notification_len += len(profile_client_booking)
                profile_client_notification_items = profile_client_booking[:3]

        if (request.user.profile_server != None):
            profile_server = request.user.profile_server.all()
            if len(profile_server) >> 0:
                profile_server = profile_server[0]
                profile_server_booking = Booking.objects.filter(profile_server=profile_server, status=0).order_by('-id')
                #profile_server_booking = list(Booking.objects.filter(profile_server=profile_server).order_by('-id'))
                notification_len += len(profile_server_booking)
                profile_server_notification_items = profile_server_booking[:3]


         # When a user is created a client_profile is created (see signals.py), so the default profile is the client_profile
        current_profile = profile_client
        current_profile_name = 'client'
        
        # defaulting to client profile
        if (not 'last_visited_profile_type' in request.session):
            request.session['last_visited_profile_type'] = 'client'

        if request.session['last_visited_profile_type'] == 'client':
            current_profile = profile_client
            current_profile_name = 'client'
        else:
            if (profile_server != None):
                current_profile = profile_server
                current_profile_name = 'server'

        
        # if (is_home):
        #     current_profile = current_profile
        #     current_profile_name = 'client'
        # else:        
        #     if (not is_viewing_as_client):
        #         if (profile_server != None):
        #             current_profile = profile_server
        #             current_profile_name = 'server'
    
    return {
            "user": current_user,
            "current_profile": current_profile,
            "current_profile_name": current_profile_name,
            "is_dashboard": is_dashboard,
            "notification_len": notification_len,
            #"is_viewing_as_client": is_viewing_as_client,
            "profile_client_notification_items": profile_client_notification_items,
            "profile_server_notification_items": profile_server_notification_items,
           }


@register.inclusion_tag('templates/secondary_navbar.html', takes_context=True)
def secondary_navbar_template(context):
    request = get_request_from_context(context)
    current_user = get_current_user(request)
    is_dashboard = 'dashboard' in request.path
    is_viewing_as_client = '/client/' in request.path
    profile_server = None
    profile_client = None

    if (not request.user.is_anonymous):
        if (request.user.profile_client != None):
            profile_client = request.user.profile_client.all()
            if len(profile_client) >> 0:
                profile_client = profile_client[0]

        if not (is_viewing_as_client):
            if (request.user.profile_server != None):
                        profile_server = request.user.profile_server.all()
                        if len(profile_server) >> 0:
                            profile_server = profile_server[0]
                            
    return {
            "user": current_user,
            "is_dashboard": is_dashboard,
            "is_viewing_as_client": is_viewing_as_client,
            "profile_client": profile_client,
            "profile_server": profile_server,
           }


@register.inclusion_tag('templates/reviews_list.html', takes_context=True)
def reviews_list_template(context, profileserver_viewing):
    review_result_list = []
    review_list = []

    request = get_request_from_context(context)
    logged_user = get_current_user(request)

    review_list = Review.objects.filter(profile_server_reviewed=profileserver_viewing) 

    for rew in review_list:
        replies = ReviewReply.objects.filter(review=rew)
        res = ReviewResult(rew, replies)
        review_result_list.append(res)

    return {
            "total_reviews": len(review_list),
            "review_result_list": review_result_list,
            "logged_user": logged_user,
            "profileserver_being_reviewed": profileserver_viewing
           }

@register.inclusion_tag('templates/new_review.html', takes_context=True)
def new_review_template(context, profileserver_viewing):
    can_write_review = False
    logged_user = None
    profile_client_logged_user = None
    past_and_finished_bookings = None

    request = get_request_from_context(context)
    logged_user = get_current_user(request)

    if (logged_user != None):
        profile_client_logged_user = logged_user.profile_client.all()[0]

        # The ProfileClient user will be able to post only if he already have at least one 
        # booking confirmed with the ProfileServer
        past_and_finished_bookings = Booking.objects.filter(profile_client=profile_client_logged_user,
                                                            profile_server=profileserver_viewing,
                                                            date_of_interest__lt=datetime.now(), 
                                                            confirmed=1)
        qtd_of_reviews_written = Review.objects.filter(profile_client_author=profile_client_logged_user).count()
        can_write_review = (past_and_finished_bookings.count() > qtd_of_reviews_written)  

    return {
            "can_write_review": can_write_review,
            "logged_user": logged_user,
            "profile_client_logged_user": profile_client_logged_user,
            "past_and_finished_bookings": past_and_finished_bookings,
            "profileserver_being_reviewed": profileserver_viewing
           }

@register.inclusion_tag('templates/footer.html', takes_context=True)
def footer_template(context):
    request = get_request_from_context(context)
    current_user = get_current_user(request)
    return {
            "user": current_user
        }

# When a template is inside another template, the request can be found at context.request intead of context['request']
# So I try to get the request from the context and if it fails, I get the request from the request parameter 
def get_request_from_context(context):    
    request = None
    if hasattr(context, 'request'):
        request = context.request
    else:
        request = context['request']
    return request

# Utility functions
def get_current_user(request):
    current_user = None
    if not (request is None):
        current_user = User.objects.filter(id=request.user.id).first()
    return current_user