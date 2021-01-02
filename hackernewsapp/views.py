
# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import ListView
from .models import Post,Vote,Comment
from .forms import CommentForm,PostForm, RegistrationForm, LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
# Create your views here.



def PostListView(request):
    posts = Post.objects.all().order_by('-created_on')
    
    for post in posts:
        post.count_votes()
        post.count_comments()
        
        
    '''
    p = Paginator(posts,4)
    page_num = request.GET.get('page',1)

    try:
        page= p.page(page_num)

    except EmptyPage:
        page= p.page(1)
    '''
    page= request.GET.get('page')
    paginator = Paginator(posts, 3)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)


    context = {
        'posts': posts,
        
        
        
    }
    return render(request,'postlist.html',context)

from datetime import datetime,timedelta
from django.utils import timezone




def PastPostListView(request):
    time = str((datetime.now(tz=timezone.utc) - timedelta(minutes=30)))
    posts = Post.objects.filter(created_on__lte = time)
    for post in posts:
        post.count_votes()
        post.count_comments()

    page= request.GET.get('page')
    paginator = Paginator(posts, 3)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context={
        'posts': posts,
    }
    return render(request,'postlist.html',context)

def UpVoteView(request,id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=id)
        votes = Vote.objects.filter(post = post)
        v = votes.filter(voter = request.user)
        if len(v) == 0:
            upvote = Vote(voter=request.user,post=post)
            upvote.save()
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect(request.META.get('HTTP_REFERER'))
    return redirect('/signin')

def DownVoteView(request,id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=id)
        votes = Vote.objects.filter(post = post)
        v = votes.filter(voter = request.user)
        if len(v) == 1:
            v.delete()
            print("delete")
            return redirect(request.META.get('HTTP_REFERER'))
        
    return redirect('/signin')   


def UserInfoView(request,username):
    user = User.objects.get(username=username)
    context = {'user':user,}
    return render(request,'user_info.html',context)


def UserSubmissions(request,username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(creator = user)
    print(len(posts))
    for post in posts:
        post.count_votes()
        post.count_comments()    
    return render(request,'user_post.html',{'posts': posts})

    
def EditListView(request,id):
    post = get_object_or_404(Post,id=id)
    if request.method =='POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    form = PostForm(instance =post)
    return render(request,'submit.html',{'form':form})


def CommentListView(request,id):
    form = CommentForm()
    post = Post.objects.get(id =id)
    post.count_votes()
    post.count_comments()

    comments = []    
    def func(i,parent):
        children = Comment.objects.filter(post =post).filter(identifier =i).filter(parent=parent)
        for child in children:
            gchildren = Comment.objects.filter(post =post).filter(identifier = i+1).filter(parent=child)
            if len(gchildren)==0:
                comments.append(child)
            else:
                func(i+1,child)
                comments.append(child)
    func(0,None)
    print(comments)

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                content = form.cleaned_data['content']
                comment = Comment(creator = request.user,post = post,content = content,identifier =0)
                comment.save()
                return redirect(f'/post/{id}')
        return redirect('/signin')
    
    
    context ={
        'form': form,
        'post': post,
        'comments': list(reversed(comments)),
    }
    return render(request,'commentpost.html', context)


def CommentReplyView(request,id1,id2):
    form = CommentForm()
    comment = Comment.objects.get(id = id2)
    post = Post.objects.get(id=id1)

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            
            if form.is_valid():
                reply_comment_content = form.cleaned_data['content']
                identifier = int(comment.identifier + 1)

                reply_comment = Comment(creator = request.user, post = post, content = reply_comment_content, parent=comment, identifier= identifier)
                reply_comment.save()

                return redirect(f'/post/{id1}')
        return redirect('/signin')
    
    context ={
        'form': form,
        'post': post,
        'comment': comment,
    }
    return render(request,'reply_post.html', context)

def SubmitPostView(request):
    if request.user.is_authenticated:
        form = PostForm()

        if request.method == "POST":
            form = PostForm(request.POST)

            if form.is_valid():
                title = request.POST['title']
                url = request.POST['url']
                description = form.cleaned_data['description']
                creator = request.user
                created_on = datetime.now()

                post = Post(title=title, url=url, description=description, creator = creator, created_on=created_on)

                post.save()
                return redirect('/')
        return render(request,'submit.html',{'form':form})
    return redirect('/signin')

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm

def signup(request):
    
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username,password = password)
            login(request, user)
            return redirect('/')
        
        else:
            messages.info(request,'Invalid details')
            return render(request,'auth_signup.html',{'form':form})
    
    else:
        form = UserCreationForm()
        return render(request,'auth_signup.html',{'form':form})

    '''
    if request.method=='POST':
        firstname=request.POST['firstname'] 
        lastname=request.POST['lastname']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username already exists')
                return redirect('http://127.0.0.1:8000/accounts/register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'email already exists')
                return redirect('http://127.0.0.1:8000/accounts/register')
            else:
                user=User.objects.create_user(username=username,password=password1,first_name=firstname,last_name=lastname,email=email)
                user.save()
                return redirect('http://127.0.0.1:8000/accounts/login')
        else:
            messages.info(request,'Password not matching....')
            return redirect('http://127.0.0.1:8000/accounts/register')    
        return redirect('http://127.0.0.1:8000/accounts/')
    else:    
        return render(request,'register.html')
    '''

    
def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)

        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid credintials....Try again')
            form = LoginForm()
            return render(request,'auth_signin.html',{'form':form})
    
    else:
        form = LoginForm()
        return render(request, 'auth_signin.html', {'form':form})


def signout(request):
    logout(request)
    return redirect('/')




def search(request):
    query = request.GET.get('query', '')
    if len(query) > 0:
        posts = Post.objects.filter(title__icontains=query).order_by('-created_on')
        for post in posts:
            post.count_votes()
            post.count_comments()

        page= request.GET.get('page')
        paginator = Paginator(posts, 3)

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        return render(request,'search.html',{'posts':posts,'query':query})
    else:
        posts = Post.objects.all().order_by('-created_on')  
        for post in posts:
            post.count_votes()
            post.count_comments() 

    return render(request,'search.html',{'posts':posts,'query':query})
