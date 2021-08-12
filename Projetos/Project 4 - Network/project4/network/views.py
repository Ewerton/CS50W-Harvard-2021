from network.FollowResult import FollowResult
from network.UserData import UserData
from network.PostResult import PostResult
from django.utils import timezone
from django.shortcuts import render, redirect
from django.template.context import Context
from network.models import Post, Comment, Preference
from users.models import Follow
import sys
from users.models import User
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django import template
from network.templatetags import network_extras
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator

register = template.Library()

ITEMS_PER_PAGE = 10

def get_posts(user):
    return Post.objects.filter(author_id=user.id)    

# gets all the posts from a user and from the given user follows
def get_posts_page_for_timeline(request):
    posts = []
    postResult = []
    page_obj = None

    if (request.user.is_authenticated):
        users_i_follow = User.objects.filter(follow_user__user=request.user)
        posts_from_users_i_follow = Post.objects.filter(author__in=users_i_follow)
        my_posts = get_posts(request.user)    
        
        posts.extend(my_posts)
        posts.extend(posts_from_users_i_follow)
        posts.sort(key=lambda x: x.date_posted, reverse=True)

        for post in posts:
            p = get_postresult(request.user, post) 
            postResult.append(p) 
    
        # Paginating the results
        paginator = Paginator(postResult, ITEMS_PER_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    return page_obj


def get_postresult(user, post):
     p = PostResult(post, post.LikedBy(user)) # checks if the current user liked the post 
     return p


def home(request):    
    page_obj = get_posts_page_for_timeline(request)

    return render(request, "network/home.html", {
        "page_obj": page_obj
    })


def about(request):
    return render(request,'network/about.html',)


# renders the profile_card template
@login_required
def profilecard(request):
    context = Context({'request': request})
    return render(request, 'network/profile_card.html' , network_extras.profilecard_template(context) )

@login_required
def whotofollow_template(request):
    context = Context({'request': request})
    return render(request, 'network/who_to_follow.html' , network_extras.who_to_follow(context) )

@csrf_exempt
@login_required
def follow_unfollow(request):
        
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    if request.user.id is None:
        return JsonResponse({"error": "No user logged in."}, status=400)
    
    if request.is_ajax() and request.method == 'POST':
        user_id_to_follow = request.POST['user_id_to_follow']
    
    if user_id_to_follow is None: 
        return JsonResponse({"error": "Id of the user to follow not provided."}, status=400)

    user_to_follow = User.objects.get(pk=user_id_to_follow)
    if (user_to_follow is None):
        return JsonResponse({"error": "Can't find the user " + user_id_to_follow + " to follow"}, status=400)

    already_following = Follow.objects.filter(user_id=request.user.id, follow_user_id=user_id_to_follow)

    if not already_following: # Not following, so, follow the user_to_follow        
        new_relation = Follow(user=request.user, follow_user=user_to_follow)
        new_relation.save()
        return JsonResponse(
            {
                "operation": "follow", 
                "message": f"The user {request.user.username} is now following {user_to_follow.username}!"
            },
            status=200)
    else:
        already_following.delete()
        return JsonResponse(
            {
                "operation": "unfollow", 
                "Message": f"The user {request.user.username} is not following {user_to_follow.username} anymore!"
            },
            status=200)

### POSTS
@login_required
def postlist_template(request):
    context = Context({'request': request})
    page_obj = get_posts_page_for_timeline(request)
    return render(request, 'network/postlist_template.html' , network_extras.postlist_template(context, page_obj) )

@login_required
def post_template(request, postResult):
    context = Context({'request': request})
    return render(request, 'network/post.html' , network_extras.post_template(context, postResult) )

@csrf_exempt
@login_required
def delete_post(request, postid):
        
    if request.method != "DELETE":
        return JsonResponse({"error": "DELETE request required."}, status=400)
    
    if request.user.id is None:
        return JsonResponse({"error": "No user logged in."}, status=400)
    
    if request.is_ajax() and request.method == 'DELETE':
        Post.objects.get(pk=postid).delete()
        return JsonResponse(
            {
                "message": f"Post Deleted!"
            }, 
            status=200)

@login_required
def save_post(request):
    if request.method == "POST":
        post_text = request.POST["text_new_tweet"]
        current_postid = request.POST["current_postid"] # if it is an update operation
        
        if (current_postid): # Updating a Post
            post = Post.objects.get(pk=current_postid)

            if (post.author != request.user):
                messages.error(request, f'You can only edit your own posts!.') 
                return redirect('home')
            
            post.content = post_text
            post.save()
        else: #New post 
            post = Post.objects.create(content=post_text,
                                    date_posted=timezone.now(),
                                    author=request.user)
            post.save()
        return redirect('home')
    else:    
        # Get Method
        context = Context({'request': request})
        return render(request, 'network/post_new.html' , network_extras.save_post_template(context) )

@csrf_exempt
@login_required
def update_post(request, postid): 
    
    post = Post.objects.get(pk=postid)

    if request.method == "POST":
        if (post.author != request.user):
            return JsonResponse({"error": "You are not the author of this post."}, status=400)

        post_text = request.POST["text_new_tweet"]        
        post.content = post_text
        post.save()
        return redirect('home')
    else:
        request.current_post = post
        return save_post(request)

@csrf_exempt
@login_required
def like_unlike(request, postid):
        
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    if request.user.id is None:
        return JsonResponse({"error": "No user logged in."}, status=400)
    
    if request.is_ajax() and request.method == 'POST':
        postid_to_like = request.POST['postid_to_like']
    
    if postid_to_like is None: 
        return JsonResponse({"error": "Id of the post to like/unlike not provided."}, status=400)

    post_to_like = Post.objects.get(pk=postid_to_like)
    if (post_to_like is None):
        return JsonResponse({"error": "Can't find the post " + post_to_like + " to like"}, status=400)

    already_liked = post_to_like.LikedBy(request.user)
       
    if not already_liked: # Not liked
        new_like = Preference(user=request.user, post=post_to_like, value=1, date=timezone.now())
        new_like.save()
        return JsonResponse(
            {
                "operation": "liked", 
                "message": f"The user {request.user.username} liked the Post {postid_to_like}!"
            }, status=200)
    else:
        preference_to_delete = Preference.objects.get(user=request.user, post=post_to_like)
        preference_to_delete.delete()
        return JsonResponse(
            {
                "operation": "unliked", 
                "Message": f"The user {request.user.username} disliked the Post {postid_to_like} !"
            }, status=200)

@login_required
def post_detail(request, postid):
    post = Post.objects.get(pk=postid) 
    postResult = get_postresult(request.user, post)

    if request.method == "POST":
        if (request.POST.get('content') != None):
            new_comment = Comment(content=request.POST.get('content'),
                                author=request.user,
                                post=post)
            new_comment.save()
        else:
            messages.error(request, f'Your reply can''t be empty.')

    comments = Comment.objects.filter(post=post).order_by('-date_posted')
    
    return render(request, "network/post_detail.html", {
        "postResult": postResult,
        "comments": comments
    })

@csrf_exempt
@login_required
def delete_comment(request, commentId):
        
    if request.method != "DELETE":
        return JsonResponse({"error": "DELETE request required."}, status=400)
    
    if request.user.id is None:
        return JsonResponse({"error": "No user logged in."}, status=400)
    
    if request.is_ajax() and request.method == 'DELETE':
        comment = Comment.objects.get(pk=commentId)
        comment.delete()

        return JsonResponse(
            {
                "message": f"Post Deleted!"
            }, 
            status=200)


### USERS
@login_required
def user_posts(request, username):
    user_to_view = User.objects.get(username=username)
    posts_results_from_user = []
    
    for post in get_posts(user_to_view):
        p = get_postresult(request.user, post) #p = PostResult(post, post.LikedBy(user)) # checks if the current user liked the post 
        posts_results_from_user.append(p)

    # Paginating the results 
    paginator = Paginator(posts_results_from_user, ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user_data = UserData(user_to_view)

    return render(request, "network/user_posts.html", {
        "user_data": user_data,
        "posts_results": posts_results_from_user,
        "page_obj": page_obj
    })


def followers(request, username):
    follow_result_list = []
    followers = Follow.objects.filter(follow_user=request.user).order_by('-date')
    for fol in followers:
        do_you_follow = Follow.objects.filter(follow_user=fol.user, user=request.user).count() > 0 # checks I follow the user who follows me
        f = FollowResult(fol.user, True, do_you_follow) 
        follow_result_list.append(f)
    
    return render(request, "network/follow.html", {
        "follow": "followers",
        "follow_results": follow_result_list,
    })


def following(request, username):
    follow_result_list = []
    following = Follow.objects.filter(user=request.user).order_by('-date')
    for fol in following:
        follow_you = Follow.objects.filter(follow_user=request.user, user=fol.follow_user).count() > 0 # checks if the followed user follows me
        f = FollowResult(fol.follow_user, follow_you, True) 
        follow_result_list.append(f)
    
    return render(request, "network/follow.html", {
        "follow_type": "following",
        "follow_results": follow_result_list,
    })

# 