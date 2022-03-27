from django.core.checks import messages
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from blog.templatetags import extras
from .models import Account, IpModel, Post, Comment

def frontpage(request):
    posts = Post.objects.all()
    return render(request, 'blog/frontpage.html', {'posts': posts})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def post_detail(request, slug):
    post = Post.objects.filter(slug=slug).first()
    author = post.author
    account = Account.objects.filter(user=author).first()
    comments = Comment.objects.filter(post=post, parent = None)
    replies = Comment.objects.filter(post=post).exclude(parent = None)
    total_likes = post.total_likes()
    total_dislikes = post.total_dislikes()
    total_subscribers = account.total_subscribers()
    total_views = post.total_views()
    liked = False
    disliked = False
    subscribed = False
    ip = get_client_ip(request)

    if IpModel.objects.filter(ip=ip).exists():
        post.views.add(IpModel.objects.get(ip=ip))
    else:
        IpModel.objects.create(ip=ip)
        post.views.add(IpModel.objects.get(ip=ip))

    if post.likes.filter(id=request.user.id).exists():
        liked = True
    if post.dislikes.filter(id=request.user.id).exists():
        disliked = True
    if account.subscribers.filter(id=request.user.id).exists():
        subscribed = True
        
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    context = {'post': post, 'comments': comments, 'replyDict': replyDict, 'total_likes': total_likes, 'liked': liked, 'total_dislikes': total_dislikes, 'disliked': disliked, 'total_subscribers': total_subscribers, 'subscribed': subscribed, 'total_views': total_views}
    return render(request, 'blog/post_detail.html', context)


def search(request):
    query = request.GET.get('query')
    if len(query) > 78:
        posts = []
    else:
        postsTitle = Post.objects.filter(title__icontains=query)
        postsBody = Post.objects.filter(body__icontains=query)
        postsAuthor = Post.objects.filter(author__username__icontains=query)
        posts = (postsTitle | postsBody | postsAuthor).distinct()
    params = {'posts': posts, 'query': query}
    return render(request, 'blog/search.html', params)


def signup(request):
    return render(request, 'blog/signup.html')


def login2(request):
    return render(request, 'blog/login.html')


def handlesignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        birthday = request.POST['birthday']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        # Checks for errornomous inputs
        if password == confirmPassword:
            myuser = User.objects.create_user(username, email, password)
            myuser.save()
            account = Account.objects.create(user=myuser)
            account.birthday = birthday
            account.save()

            loginUsername = username
            loginPassword = password
            user = authenticate(username=loginUsername, password=loginPassword)
            login(request, user)
            messages.success(request, 'Your Edge Blogs account has been succesfully created')
            return redirect('/')
        else:
            messages.error(request, 'Your passwords do not match please try again')
            return redirect('/signup')
    else:
        return redirect('/')


def handlelogin(request):
    if request.method == 'POST':
        loginUsername = request.POST['loginUsername']
        loginPassword = request.POST['loginPassword']

        user = authenticate(username=loginUsername, password=loginPassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in succesfully")
            return redirect('/')
        else:
            messages.error(request, 'No matching user found')
            return redirect('/')
    else:
        return redirect('/')


def handlelogout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Logged out succesfully")
        return redirect('/')
    else:
        messages.error(request, "Logged out failed! Try again with a correct method")
        return redirect('/')

def add_blog(request):
    return render(request, 'blog/add_blog.html')

def haf(request):
    return render(request, 'blog/haf.html')

def tandc(request):
    return render(request, 'blog/termsandconditions.html')

def faq(request):
    return render(request, 'blog/faq.html')

def privacypolicy(request):
    return render(request, 'blog/privacypolicy.html')

def contactus(request):
    return render(request, 'blog/contactus.html')

def disclamer(request):
    return render(request, 'blog/disclamer.html')

def addPostDone(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.user
        description = request.POST['description']
        body = request.POST['content']

        mypost = Post.objects.create()
        mypost.title = title
        mypost.author = author
        mypost.intro = description
        mypost.body = body
        mypost.save()
        messages.success(request, "Your Blog has been Posted Succesfully!")
        return redirect('/')
    else:
        messages.error(request, "There was an error in the creation of Blog! Try again with a correct method!")
        return redirect('/')
        

def addPost(request):
    return render(request, 'blog/addPost.html')

def yourBlogs(request):
    postsAuthor = Post.objects.filter(author__username__icontains=request.user)
    posts = (postsAuthor).distinct()
    params = {'posts': posts}
    return render(request, 'blog/yourBlogs.html', params)

def postComment(request):
    if request.method == "POST":
        content = request.POST.get("content")
        user = request.user
        postSlug = request.POST.get("postSlug")
        post = Post.objects.get(slug=postSlug)
        parentSno = request.POST.get("parentSno")

        if parentSno == "":
            if(len(content.strip())):
                mycomment = Comment.objects.create()
                mycomment.content = content
                mycomment.user = user
                mycomment.post = post
                mycomment.save()
                messages.success(request, "Your comment has been posted succesfully!")
        else:
            if(len(content.strip())):
                parent = Comment.objects.get(sno=parentSno)
                mycomment = Comment.objects.create()
                mycomment.content = content
                mycomment.user = user
                mycomment.post = post
                mycomment.parent = parent
                mycomment.save()
                messages.success(request, "Your reply has been posted succesfully!")

    return redirect('/' + str(post.slug))

def LikeView(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=request.POST.get('post_id'))
        liked = False
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            if post.dislikes.filter(id=request.user.id).exists():
                post.dislikes.remove(request.user)
            post.likes.add(request.user)
            liked = True
        return redirect('/' + str(post.slug))
    else:
        messages.error(request, "You must be logged in to like a post!")
        return render(request, 'blog/login.html')

def DislikeView(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=request.POST.get('post_id'))
        disliked = False
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
            disliked = False
        else:
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
            post.dislikes.add(request.user)
            disliked = True
        print("disliked")
        return redirect('/' + str(post.slug))
    else:
        messages.error(request, "You must be logged in to dislike a post!")
        return render(request, 'blog/login.html')

def SubscribeView(request, author_name):
    if request.user.is_authenticated:
        author = User.objects.get(username=author_name)
        postSlug = request.POST.get("postSlug")
        account = Account.objects.get(user=author)
        subscribed = False
        if account.subscribers.filter(id=request.user.id).exists():
            account.subscribers.remove(request.user)
            subscribed = False
            messages.success(request, "Successfully Unsubscribed to " + str(author.username) + "!")
        else:
            account.subscribers.add(request.user)
            subscribed = True
            messages.success(request, "Successfully Subscribed to " + str(author.username) + "!")
        return redirect('/' + str(postSlug)) 
    else:
        messages.error(request, "You must be logged in to subscribe to a post!")
        return render(request, 'blog/login.html')

    
