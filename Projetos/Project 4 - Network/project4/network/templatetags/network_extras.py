from datetime import datetime
from django.template.defaultfilters import date
from network.models import Post
from users.models import Follow, User
from django import template
from django.db.models import Count

register = template.Library()

@register.inclusion_tag('network/navbar.html', takes_context=True)
def navbar_template(context):
    request = context['request']
    current_user = get_current_user(request)
    return {'user': current_user}

@register.inclusion_tag('network/profile_card.html', takes_context=True)
def profilecard_template(context, user):
    request = context['request']
    current_user = get_current_user(request)
    user_to_view = user
    can_current_user_follow = Follow.objects.filter(user=current_user, follow_user=user_to_view).count() == 0
    return {
            "user_to_view": user_to_view,    
            "user": current_user,
            "can_current_user_follow": can_current_user_follow  
            }

# Returns a list of user which posts frequently, except the current logged user
@register.inclusion_tag('network/who_to_follow.html', takes_context=True)
def who_to_follow(context):
    request = context['request']

    users_i_follow = Follow.objects.filter(user_id=request.user.id)

    users_to_follow = []
    data_counter = Post.objects.values('author')\
        .annotate(author_count=Count('author'))\
        .order_by('-author_count')[:6] # User who posts a lot, maximum of 6

    for aux in data_counter:
        if (aux['author'] != request.user.id): # if the current user is not the current logged user
            already_following = any(u.follow_user_id == aux['author'] for u in users_i_follow)
            if already_following:
                continue
            else:
                user_to_follow = User.objects.filter(pk=aux['author']).first()
                users_to_follow.append(user_to_follow)
    
    return {"users_to_follow": users_to_follow,
            "user": request.user }

# Render the form to add a new post
@register.inclusion_tag('network/post_new.html', takes_context=True)
def save_post_template(context):
    request = context['request']
    current_user = get_current_user(request)
    current_post = None
    if hasattr(request, 'current_post'):
        current_post = request.current_post
    return {
        "user": current_user, 
        "current_post": current_post 
        }

# Render the form to add a new post
@register.inclusion_tag('network/post.html', takes_context=True)
def post_template(context, postResult):
    #request = context['request']
    #current_user = get_current_user(request)
    return {
        "user": context.request.user, 
        "postResult": postResult, 
        }

@register.inclusion_tag('network/postlist_template.html', takes_context=True)
def postlist_template(context, posts_results):
    #request = context['request']
    #current_user = context.request.user
    return {
            "user": context.request.user,
            "post_results": posts_results   
            }

# Utility functions
def get_current_user(request):
    current_user = None
    if not (request is None):
        current_user = User.objects.filter(id=request.user.id).first()
    return current_user