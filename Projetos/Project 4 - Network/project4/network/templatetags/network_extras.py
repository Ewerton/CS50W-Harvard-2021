from datetime import datetime
from django.template.defaultfilters import date
from network.models import Post
from users.models import User
from django import template
from django.db.models import Count

register = template.Library()


@register.inclusion_tag('network/results.html', takes_context=True)
def show_results(context):
    request = context['request']
    choices = ['a', 'b', 'c', request.user.username, datetime.now().strftime("%d/%m/%Y %H:%M:%S") ]
    return {'choices': choices}

@register.inclusion_tag('network/navbar.html', takes_context=True)
def navbar(context):
    request = context['request']
    #choices = ['a', 'b', 'c', request.user.username]
    return {'user': request.user}

@register.inclusion_tag('network/profile_card.html', takes_context=True)
def profile_card(context):
    request = context['request']
    current_user = User.objects.filter(id=request.user.id).first()
    return {"current_user": current_user }

# Returns a list of user which posts frequently, except the current logged user
@register.inclusion_tag('network/who_to_follow.html', takes_context=True)
def who_to_follow(context):
    request = context['request']
    users_to_follow = []
    data_counter = Post.objects.values('author')\
        .annotate(author_count=Count('author'))\
        .order_by('-author_count')[:6] # User who posts a lot, maximum of 6

    for aux in data_counter:
        if (aux['author'] != request.user.id): # if the current user is not the current logged user
            users_to_follow.append(User.objects.filter(pk=aux['author']).first())
    
    return {"users_to_follow": users_to_follow }