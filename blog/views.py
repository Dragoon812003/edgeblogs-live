from django.core.checks import messages
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Post

def frontpage(request):
    posts = Post.objects.all()
    return render(request, 'blog/frontpage.html', {'posts': posts})


def post_detail(request, slug):
    post = Post.objects.filter(slug=slug).first()
    context = {'post': post}
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
            myuser.birthday = birthday
            myuser.save()
            messages.success(request, 'Your Edge Blogs account has been succesfully created. Please Login')
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
        return redirect('/')
    else:
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
        return redirect('/')
    else:
        return redirect('/')
        

def addPost(request):
    return render(request, 'blog/addPost.html')

def yourBlogs(request):
    postsAuthor = Post.objects.filter(author__username__icontains=request.user)
    posts = (postsAuthor).distinct()
    params = {'posts': posts}
    return render(request, 'blog/yourBlogs.html', params)
