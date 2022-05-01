from django.core.checks import messages
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from blog.templatetags import extras
from .models import Account, IpModel, Post, Comment, Category
from BlogPage.utils import get_category, get_client_ip, remove_html_tags
from BlogPage.recommneding import *

def frontpage(request):
    posts = Post.objects.all()
    if request.user.is_authenticated:
        viewed_posts = request.user.account.history.all()
        sort_key = []
        for post in posts:
            sort_key.append(get_score(post, request.user))
        posts = sorted(posts, key=lambda x: get_score(x, request.user), reverse=True)
        return render(request, 'blog/frontpage.html', {'posts': posts, 'viewed_posts': viewed_posts})
    else:
        posts = sorted(posts, key=score, reverse=True)
        return render(request, 'blog/frontpage.html', {'posts': posts})

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
    categories = Category.objects.filter(posts=post)
    
    if request.user.is_authenticated:
        request.user.account.history.add(post)
        request.user.account.save()
        for category in categories:
            request.user.account.categories_liked.add(category)
            request.user.account.save()
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
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        
        # Checks for errornomous inputs
        if password == confirmPassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('/signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists!')
                return redirect('/signup')
            elif username.__contains__(' '):
                messages.error(request, 'Username cannot contain a space!')
                return redirect('/signup')
            elif len(username) < 3:
                messages.error(request, 'Username must be at least 3 characters long!')
                return redirect('/signup')
            elif len(username) > 16:
                messages.error(request, 'Username cannot be more than 16 characters long!')
                return redirect('/signup')
            else:
                myuser = User.objects.create_user(username, email, password)
                myuser.save()
                account = Account.objects.create(user=myuser)
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

def signingup(request):
    if request.method == "POST":
        type = request.POST['type']
        if type == 'username':
            username = request.POST['username']
            if User.objects.filter(username=username).exists():
                data = {'status': 'error', "message": "Username already exists!", "username": username}
            elif username == "":
                data = {'status': 'error', "message": "Username cannot be empty", "username": username}
            elif len(username) < 3:
                data = {'status': 'error', "message": "Username must be at least 3 characters", "username": username}
            elif len(username) > 16:
                data = {'status': 'error', "message": "Username must be less than 16 characters", "username": username}
            else:
                data = {'status': 'success', "message": "Username is available!", "username": username}
            return JsonResponse(data, safe=False)
        elif type == 'email':
            email = request.POST['email']
            if User.objects.filter(email=email).exists():
                data = {'status': 'error', "message": "Email already exists!", "email": email}
            elif email == "":
                data = {'status': 'error', "message": "Email cannot be empty", "email": email}
            else:
                data = {'status': 'success', "message": "Email is available!", "email": email}
            return JsonResponse(data, safe=False)
    else:
        return redirect('/signup')
    

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
            return redirect('/login2')
    else:
        return redirect('/')


def handlelogout(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "Logged out succesfully")
        return redirect('/')
    else:
        messages.error(request, "Logged out failed! Please try again")
        return redirect('/')
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

        mypost.author.account.save()
        mypost.save()
        new_categories = get_category(mypost)
        total_words = 0
        for new_category in new_categories:
            total_words += int(new_category['count'])
        for new_category in new_categories:
            if new_categories not in Category.objects.all():
                new_category_add = Category.objects.create()
                new_category_add.word = new_category['word']
                new_category_add.count = new_category['count']
                new_category_add.probability = new_category['count']/total_words
                new_category_add.save()
                mypost.categories.add(new_category_add)
            
            mypost.save()
        
        messages.success(request, "Your Blog has been Posted Succesfully!")
        return redirect('/post/' + mypost.slug)
    else:
        messages.error(request, "There was an error in the creation of Blog! Please try again!")
        return redirect('/')
        
def addPost(request):
    return render(request, 'blog/addPost.html')

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

    return redirect('/post/' + str(post.slug))

def LikeView(request, slug):
    if request.user.is_authenticated:
        post = Post.objects.filter(slug=slug).first()
        
        liked = False

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            if post.dislikes.filter(id=request.user.id).exists():
                post.dislikes.remove(request.user)
            post.likes.add(request.user)
            liked = True
        data = {'status': 'success', 'liked': liked, 'total_likes': post.total_likes(), 'disliked': False, 'total_dislikes': post.total_dislikes()}
    else:
        data = {'status': 'error', 'message': 'You must be logged in to like a post. Click <a href="/signup" class="underline hover:text-blue-700">here</a> to Sign Up!'}
    return JsonResponse(data, safe=False)

def DislikeView(request, slug):
    if request.user.is_authenticated:
        post = Post.objects.filter(slug=slug).first()

        disliked = False
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
            disliked = False
        else:
            if post.likes.filter(id=request.user.id).exists():
                post.likes.remove(request.user)
                liked = False
            post.dislikes.add(request.user)
            disliked = True
        data = {'status': 'success', 'liked': False, 'total_likes': post.total_likes(), 'disliked': disliked, 'total_dislikes': post.total_dislikes()}
    else:
        data = {'status': 'error', 'message': 'You must be logged in to dislike a post. Click <a href="/signup" class="underline hover:text-blue-700">here</a> to Sign Up!'}
    return JsonResponse(data, safe=False)

def SubscribeView(request, author_name):
    if request.user.is_authenticated:
        author = User.objects.get(username=author_name)
        postSlug = request.POST.get("postSlug")
        account = Account.objects.get(user=author)
        subscribed = False
        if account.subscribers.filter(id=request.user.id).exists():
            account.subscribers.remove(request.user)
            subscribed = False
        else:
            account.subscribers.add(request.user)
            subscribed = True
        data = {'status': 'success', 'subscribed': subscribed, 'total_subscribers': account.total_subscribers()}
    else:
        data = {'status': 'error', 'message': 'You must be logged in to subscribe to a author. Click <a href="/signup" class="underline hover:text-blue-700">here</a> to Sign Up!'}
    return JsonResponse(data, safe=False)

def AuthorPostView(request, author_name):
    author = User.objects.get(username=author_name)
    postsAuthor = Post.objects.filter(author__username__icontains=author_name)
    posts = postsAuthor.distinct()
    params = {'posts': posts, 'author': author}
    return render(request, 'blog/authorBlogs.html', params)

def recalculate_categories(request):
    if request.user.is_superuser:
        print("Recalculating categories...")
        Categories = Category.objects.all()
        Posts = Post.objects.all()
        for edit_category in Categories:
            edit_category.delete()
        print("")
        print("All Categories Deleted")
        print("")
        for post in Posts:
            new_categories = get_category(post)
            total_words = 0
            print("")
            print("Post: " + post.title)
            print("")
            for new_category in new_categories:
                total_words += int(new_category['count'])
            for new_category in new_categories:
                if new_categories not in Categories:
                    new_category_add = Category.objects.create()
                    new_category_add.word = new_category['word']
                    new_category_add.count = new_category['count']
                    new_category_add.probability = new_category['count']/total_words
                    new_category_add.save()
                    post.categories.add(new_category_add)
                    print("new category", new_category_add)
                    print("new category count", new_category_add.count)
                    print("total words", total_words)
                    print("")
                
                post.save()
            print("********** Post Saved **********")
            print("")
        print("All Categories Recalculated")
        return redirect('/')
    else:
        return HttpResponse("GET OUT OF HERE!")
    
def read_file(request):
    f = open('validation.txt', 'r')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")

