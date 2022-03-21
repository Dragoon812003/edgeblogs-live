from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from blog.views import frontpage, post_detail, search, signup, login2, handlesignup, handlelogin, handlelogout, add_blog, faq, tandc, haf, privacypolicy, contactus, disclamer, addPostDone, addPost, yourBlogs, postComment, LikeView, DislikeView, SubscribeView

admin.site.site_header = "Edge Blogs Admin"
admin.site.site_title = "Edge Blogs Admin Panel"
admin.site.index_title = " Welcome to Edge Blogs Admin Panel"

urlpatterns = [
    path('', frontpage, name='frontpage'),
    path('admin/', admin.site.urls),
    path('<slug:slug>/', post_detail, name='post_detail'),
    path('search', search, name='search'),
    path('signup', signup, name='signup'),
    path('login2', login2, name='login2'),
    path('signupdone', handlesignup, name='handlesignup'),
    path('logindone', handlelogin, name='handlelogin'),
    path('logout', handlelogout, name='handlelogout'),
    path('faq', faq, name='faq'),
    path('tandc', tandc, name='tandc'),
    path('haf', haf, name='haf'),
    path('disclamer', disclamer, name='disclamer'),
    path('contactus', contactus, name='contactus'),
    path('privacypolicy', privacypolicy, name='privacypolicy'),
    path('addPost', addPost, name='addPost'),
    path('addPostDone', addPostDone, name='addPostDone'),
    path('postComment', postComment, name='postComment'),
    path('yourBlogs', yourBlogs, name='yourBlogs'),
    path('like/<int:pk>', LikeView, name='like_post'),
    path('dislike/<int:pk>', DislikeView, name='dislike_post'),
    path('subscribe/<str:author_name>', SubscribeView, name='subscribe_author'),
]
