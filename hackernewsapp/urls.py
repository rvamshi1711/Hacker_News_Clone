from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',PostListView, name='home'),
    path('search/', search, name='search'),
    path('past',PastPostListView, name='past_home'),
    path('user/<username>', UserInfoView, name='user_info'),
    path('posts/<username>',UserSubmissions, name='user_post'),
    path('post/<int:id>',CommentListView, name='post'),
    path('submit',SubmitPostView, name='submit'),
    path('signin',signin, name='signin'),
    path('signup',signup, name='signup'),
    path('signout',signout, name='signout'),
    path('vote/<int:id>',UpVoteView,name='vote'),
    path('dvote/<int:id>',DownVoteView,name='dvote'),
    path('post/<int:id1>/comment/<int:id2>',CommentReplyView,name='reply'),
    path('edit/<int:id>',EditListView, name='edit')
]
