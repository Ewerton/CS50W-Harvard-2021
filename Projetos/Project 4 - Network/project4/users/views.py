from users.SearchResult import SearchResult
from django.contrib.messages.api import error
from users.models import Follow, Profile
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from users.models import User
from project4 import Utils

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def register(request):
    if request.method == 'POST':
        newUser = User()
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if (Utils.strIsNoneBlankWhithespace(username)):
             messages.error(request, f'Username is invalid.')
        else:
            existentUsername = User.objects.filter(username=username)
            if (len(existentUsername) > 0):
                messages.error(request, f'Username already taken.')

        if (not Utils.is_email(email)):
            messages.error(request, f'Email is invalid.')
        else:
            existentEmail = User.objects.filter(email=email)
            if (len(existentEmail) > 0):
                messages.error(request, f'This email is already in use.')

        if (Utils.strIsNoneBlankWhithespace(pass1)):
            messages.error(request, f'Choose a password.')
        else:
            if (pass1 != pass2):
                messages.error(request, f'Password and confirmation password does not match.')
        
        if (not Utils.contains_errormessage(request)):
            newUser.username = username
            newUser.email = email
            #newUser.password = pass1
            newUser.set_password(pass1)
            newUser.save()
            messages.success(request, f'Account created for {username}.')
            return redirect('login')
        else:
             return render(request, 'users/register.html', {
        })

    else:
        return render(request, 'users/register.html', {
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            # redirect the user to the previous URL saved in the session that could be the "/" or some custom location
            return HttpResponseRedirect(reverse("home"))
            # return render(request, "network/home.html", {
            #    # "message": "Invalid username and/or password."
            # })
        else:
            messages.error(request, f'Invalid username and/or password.')
            return render(request, "users/login.html", {
               # "message": "Invalid username and/or password."
            })
    else:
        return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


@login_required
def settings(request):
    current_user_profile = Profile.objects.get(user_id=request.user.id)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        image = None

        if (len(request.FILES) != 0):
            image = request.FILES["image"]
        
        if (not Utils.is_email(email)):
            messages.error(request, f'Email is invalid.')

        if (Utils.strIsNoneBlankWhithespace(username)):
            messages.error(request, f'username is invalid.')

        if (image is not None):
            if (not Utils.is_image(image)):
                messages.error(request, f'invalid image.')

        if (not Utils.contains_errormessage(request)):
            current_user_profile.user.username = username
            current_user_profile.user.email = email
            if (image is not None):
                current_user_profile.image = image

            current_user_profile.save()
            messages.success(request, f'Account has been updated.')
        
        return render(request, 'users/settings.html', {
            'uprof': current_user_profile
        })
        
    else:
        return render(request, 'users/settings.html', {
            'uprof': current_user_profile
        })



# @login_required
# def SearchView(request):
#     if request.method == 'POST':
#         search_string = request.POST.get('search')

#         query_results = User.objects.filter(username__icontains=search_string)\
#             .exclude(username=request.user.username) # excludes the current logged user
             
#         users_i_follow = Follow.objects.filter(user_id=request.user.id)
        
#         results = []

#         for item in query_results:
#             already_following = any(item.id == u.follow_user_id for u in users_i_follow)
#             if already_following:
#                 t = (item, True)               
#             else:
#                 t = (item, False)                
#             results.append(t)

#         context = {
#             'results':results
#         }
#     return render(request, 'users/search_result.html', context)
@login_required
def SearchView(request):
    if request.method == 'POST':
        search_string = request.POST.get('search')

        query_results = User.objects.filter(username__icontains=search_string)\
            .exclude(username=request.user.username) # excludes the current logged user
             
        users_i_follow = Follow.objects.filter(user_id=request.user.id)
        
        results = []

        for item in query_results:
            already_following = any(item.id == u.follow_user_id for u in users_i_follow)
            if already_following:
                res = SearchResult(item, True)               
            else:
                res = SearchResult(item, False)           
            results.append(res)

        context = {
            'results':results
        }
    return render(request, 'users/search_result.html', context)
