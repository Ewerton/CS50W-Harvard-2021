from django.urls import path
from .import views
from django.urls import include

urlpatterns = [
    path('', views.home, name='home'),
    path('about/',views.about, name='about'),
   
    path('user/<str:username>', views.user_posts, name='user-posts'),
    path('user/<str:username>/following', views.following, name='user-following'),
    path('user/<str:username>/followers', views.followers, name='user-followers'),

    path('get_profilecard', views.profilecard, name='get_profilecard'),
    path('get_whotofollow', views.whotofollow_template, name='get_whotofollow'),
    path('follow_unfollow', views.follow_unfollow, name='follow_unfollow'),
    path('get_postlist', views.postlist_template, name='get_postlist'),

    path('post/save/', views.save_post, name='post-create'),
    path('post/<int:postid>/', views.post_detail, name='post-detail'),
    path('post/<int:postid>/update/', views.update_post, name='post-update'),
    path('post/<int:postid>/del/', views.delete_post, name='post-delete'),
    path('post/<int:postid>/like/', views.like_unlike, name='post-like'), 
    path('comment/<int:commentId>/del/', views.delete_comment, name='comment-delete'),
]