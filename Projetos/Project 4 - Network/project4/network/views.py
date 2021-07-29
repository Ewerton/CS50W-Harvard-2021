from network.PostResult import PostResult
from django.utils import timezone
#import pytz
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context import Context
from network.models import Post, Comment, Preference
from users.models import Follow, Profile
import sys
#from django.contrib.auth.models import User
from users.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from .forms import NewCommentForm
from django.contrib.auth.decorators import login_required
#from .serializers import UserSerializer, GroupSerializer, PostSerializer
from django.contrib.auth.models import Group
#from rest_framework import viewsets
#from rest_framework import permissions
#from rest_framework.decorators import api_view
from django.http.response import HttpResponse, JsonResponse
#from rest_framework.parsers import JSONParser 
#from rest_framework import status
from django import template
from django.template import RequestContext, Template
from network.templatetags import network_extras
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
register = template.Library()

PAGINATION_COUNT = 3

# gets all the posts from a user and from the given user follows
def get_posts(user):
    posts = []
    postResult = []
    users_i_follow = User.objects.filter(follow_user__user=user)
    posts_from_users_i_follow = Post.objects.filter(author__in=users_i_follow)
    my_posts = Post.objects.filter(author_id=user.id)    
    
    posts.extend(my_posts)
    posts.extend(posts_from_users_i_follow)
    
    for post in posts:
        #liked = PostResult.UserLiked(user)
        p = PostResult(post, post.LikedBy(user)) # checks if the current user liked the post 
        postResult.append(p)
 
    postResult.sort(key=lambda x: x.post.date_posted, reverse=True)
    return postResult



def home(request):    
    post_list = []

    current_user = User.objects.filter(id=request.user.id).first()
    if (current_user != None):
        post_list = get_posts(current_user) 

    return render(request, "network/home.html", {
        "post_list": post_list,
    })

def is_users(post_user, logged_user):
    return post_user == logged_user





class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'network/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = PAGINATION_COUNT

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        users_to_follow = []
        data_counter = Post.objects.values('author')\
            .annotate(author_count=Count('author'))\
            .order_by('-author_count')[:6] # User who posts a lot

        for aux in data_counter:
            if (aux['author'] != self.request.user.id): # if the current user is not the current logged user
                users_to_follow.append(User.objects.filter(pk=aux['author']).first())
        
        # if Preference.objects.get(user = self.request.user):
        #     data['preference'] = True
        # else:
        #     data['preference'] = False
        data['preference'] = Preference.objects.all()
        # print(Preference.objects.get(user= self.request.user))
        data['users_to_follow'] = users_to_follow
        print(users_to_follow, file=sys.stderr)
        return data

    def get_queryset(self):
        user = self.request.user
        qs = Follow.objects.filter(user=user)
        follows = [user]
        for obj in qs:
            follows.append(obj.follow_user)
        return Post.objects.filter(author__in=follows).order_by('-date_posted')


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = PAGINATION_COUNT

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        visible_user = self.visible_user()
        logged_user = self.request.user
        print(logged_user.username == '', file=sys.stderr)

        if logged_user.username == '' or logged_user is None:
            can_follow = False
        else:
            can_follow = (Follow.objects.filter(user=logged_user,
                                                follow_user=visible_user).count() == 0)
        data = super().get_context_data(**kwargs)

        data['user_profile'] = visible_user
        data['can_follow'] = can_follow
        return data

    def get_queryset(self):
        user = self.visible_user()
        return Post.objects.filter(author=user).order_by('-date_posted')

    def post(self, request, *args, **kwargs):
        if request.user.id is not None:
            follows_between = Follow.objects.filter(user=request.user,
                                                    follow_user=self.visible_user())

            if 'follow' in request.POST:
                    new_relation = Follow(user=request.user, follow_user=self.visible_user())
                    if follows_between.count() == 0:
                        new_relation.save()
            elif 'unfollow' in request.POST:
                    if follows_between.count() > 0:
                        follows_between.delete()

        return self.get(self, request, *args, **kwargs)


class PostDetailView(DetailView):
    model = Post
    template_name = 'network/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        comments_connected = Comment.objects.filter(post_connected=self.get_object()).order_by('-date_posted')
        data['comments'] = comments_connected
        data['form'] = NewCommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(content=request.POST.get('content'),
                              author=self.request.user,
                              post_connected=self.get_object())
        new_comment.save()

        return self.get(self, request, *args, **kwargs)


# class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Post
#     template_name = 'network/post_delete.html'
#     context_object_name = 'post'
#     success_url = '/'

#     def test_func(self):
#         return is_users(self.get_object().author, self.request.user)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']
    template_name = 'network/post_new.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Add a new post'
        return data


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']
    template_name = 'network/post_new.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Edit a post'
        return data


class FollowsListView(ListView):
    model = Follow
    template_name = 'network/follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'follows'
        return data


class FollowersListView(ListView):
    model = Follow
    template_name = 'network/follow.html'
    context_object_name = 'follows'

    def visible_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        user = self.visible_user()
        return Follow.objects.filter(follow_user=user).order_by('-date')

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['follow'] = 'followers'
        return data


# Like Functionality====================================================================================

@login_required
def postpreference(request, postid, userpreference):
        
        if request.method == "POST":
                eachpost= get_object_or_404(Post, id=postid)

                obj=''

                valueobj=''

                try:
                        obj= Preference.objects.get(user= request.user, post= eachpost)

                        valueobj= obj.value #value of userpreference


                        valueobj= int(valueobj)

                        userpreference= int(userpreference)
                
                        if valueobj != userpreference:
                                obj.delete()


                                upref= Preference()
                                upref.user= request.user

                                upref.post= eachpost

                                upref.value= userpreference


                                if userpreference == 1 and valueobj != 1:
                                        eachpost.likes += 1
                                        eachpost.dislikes -=1
                                elif userpreference == 2 and valueobj != 2:
                                        eachpost.dislikes += 1
                                        eachpost.likes -= 1
                                

                                upref.save()

                                eachpost.save()
                        
                        
                                context= {'eachpost': eachpost,
                                  'postid': postid}

                                return redirect('home')

                        elif valueobj == userpreference:
                                obj.delete()
                        
                                if userpreference == 1:
                                        eachpost.likes -= 1
                                elif userpreference == 2:
                                        eachpost.dislikes -= 1

                                eachpost.save()

                                context= {'eachpost': eachpost,
                                  'postid': postid}

                                return redirect('home')
                                
                        
        
                
                except Preference.DoesNotExist:
                        upref= Preference()

                        upref.user= request.user

                        upref.post= eachpost

                        upref.value= userpreference

                        userpreference= int(userpreference)

                        if userpreference == 1:
                                eachpost.likes += 1
                        elif userpreference == 2:
                                eachpost.dislikes +=1

                        upref.save()

                        eachpost.save()                            


                        context= {'eachpost': eachpost,
                          'postid': postid}

                        return redirect('home')


        else:
                eachpost= get_object_or_404(Post, id=postid)
                context= {'eachpost': eachpost,
                          'postid': postid}

                return redirect('home')



def about(request):
    return render(request,'network/about.html',)



# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]

def post_list(request):
    pass



# renders the show_results template
def test_ajax(request):
    context = Context({'request': request})
    return render(request, 'network/results.html' , network_extras.show_results(context) )

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

# render the post_new template
@login_required
def save_post(request):
    if request.method == "POST":
        post_text = request.POST["text_new_tweet"]
        current_postid = request.POST["current_postid"] # if it is an update operation
        
        if (current_postid):
            post = Post.objects.get(pk=current_postid)
            post.content = post_text
            post.save()
        else:
            post = Post.objects.create(content=post_text,
                                    date_posted=timezone.now(),
                                    author=request.user, 
                                    likes=0)
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

#render_to_string 
    # return render(request, "network/home.html", {
    #     "post_list": post_list,
    # })


# @api_view(['GET', 'POST', 'DELETE'])
# def post_list(request):
#     if request.method == 'GET':
#         posts = Post.objects.all()
        
#         title = request.query_params.get('title', None)
#         if title is not None:
#             posts = posts.filter(title__icontains=title)
        
#         posts_serializer = PostSerializer(posts, many=True)
#         return JsonResponse(posts_serializer.data, safe=False)
#         # 'safe=False' for objects serialization
 
#     elif request.method == 'POST':
#         post_data = JSONParser().parse(request)
#         post_serializer = PostSerializer(data=post_data)
#         if post_serializer.is_valid():
#             post_serializer.save()
#             return JsonResponse(post_serializer.data, status=status.HTTP_201_CREATED) 
#         return JsonResponse(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == 'DELETE':
#         count = Post.objects.all().delete()
#         return JsonResponse({'message': '{} Posts were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


