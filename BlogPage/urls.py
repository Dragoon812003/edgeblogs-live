from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from blog.views import *

admin.site.site_header = "Edge Blogs Admin"
admin.site.site_title = "Edge Blogs Admin Panel"
admin.site.index_title = " Welcome to Edge Blogs Admin Panel"

urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('admin/', admin.site.urls),
    path('like/<slug:slug>', LikeView, name='like_post'),
    path('dislike/<slug:slug>', DislikeView, name='dislike_post'),
    path('subscribe/<str:author_name>', SubscribeView, name='subscribe_author'),
    path('post/<slug:slug>/', post_detail, name='post_detail'),
    path('search', search, name='search'),
    path('signup', signup, name='signup'),
    path('login2', login2, name='login2'),
    path('signupdone', handlesignup, name='handlesignup'),
    path('logindone', handlelogin, name='handlelogin'),
    path('logout', handlelogout, name='handlelogout'),
    path('FrequentlyAskedQuestions', faq, name='faq'),
    path('TermsandConditions', tandc, name='tandc'),
    path('HelpandFeedback', haf, name='haf'),
    path('Disclaimer', disclamer, name='disclamer'),
    path('contactus', contactus, name='contactus'),
    path('PrivacyPolicy', privacypolicy, name='privacypolicy'),
    path('addPost', addPost, name='addPost'),
    path('addPostDone', addPostDone, name='addPostDone'),
    path('postComment', postComment, name='postComment'),
    path('author/<str:author_name>', AuthorPostView, name='author_post_view'),
    path('recalculate', recalculate_categories, name='recalculate'),
    path('signingup', signingup, name='signingup'),
]
