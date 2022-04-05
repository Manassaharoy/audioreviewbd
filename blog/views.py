from poplib import POP3_SSL_PORT
from django.shortcuts import redirect, render
from blog.models import Post, Categories, Author, Subscribe, Contact, Comment, SubComment
import datetime

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from django.contrib import messages

from django.http import Http404

from .forms import CreateForm

from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        messages.add_message(request, messages.SUCCESS, 'Successfully submitted!')
        Subscribe(email = email).save()

    month_ago = datetime.date.today() - datetime.timedelta(days = 30)

    trending_post = Post.objects.filter(time_upload__gte = month_ago).order_by('-read')

    top_authors = Author.objects.order_by('-rate')[:4]
    authors_top_post = [Post.objects.filter(author = author).first() for author in top_authors]
    all_posts = Post.objects.all()
    # published_posts = Post.objects.filter(publish = True)
    all_time_best = Post.objects.all().order_by('-read')[0]
    recent_best = Post.objects.all().order_by('-read')

    paginated_post = Paginator(Post.objects.filter(publish = True), 6)
    page = request.GET.get('page')
    try:
        published_posts = paginated_post.page(page)
    except PageNotAnInteger:
        published_posts = paginated_post.page(1)
    except EmptyPage:
        published_posts = paginated_post.page(paginated_post.num_pages)

    context = {
        'title' : 'Welcome | Audio Review BD',
        # 'all_posts' : all_posts,
        'posts' : published_posts,
        'all_time_best' : all_time_best,
        'recent_best' : recent_best,
        'authors_top_post' : authors_top_post,
        'trending_post' : trending_post[:5],
        

    }
    return render(request, 'index.html',context)
    
def search(request):
    recent_best = Post.objects.all().order_by('-read')

    q = request.GET.get('search')
    posts = Post.objects.filter(
        Q(title__icontains = q) | Q(overview__icontains = q)
    ).distinct()
    return render(request, 'search.html', 
    {
        'posts': posts,
        'recent_best': recent_best,
        'title': f"Search results for {q}",

    })

def about(request):
    context = {
        'title': 'About | Audio Review BD'

    }
    return render(request, 'about.html', context)


def blog(request, id, slug):
    recent_best = Post.objects.all().order_by('-read')
    try:
        post = Post.objects.get(pk = id, slug = slug)
    except:
        raise Http404("Post does not exist!")
    post.read += 1
    post.save()

    comments = []

    for comment in Comment.objects.filter(post = post):
        comments.append([comment, SubComment.objects.filter(comment=comment)])

    if request.method == 'POST':
        cmt = request.POST.get('comment')
        rply = request.POST.get('comm_id')
        if rply:
            SubComment(
                post=post,
                user= request.user,
                reply = cmt,
                comment = Comment.objects.get(id=int(rply))
             ).save()
        else:
            Comment(post=post, user=request.user, comment=cmt).save()

    return render(request, 'blog-single.html', {'post' : post, 'recent_best' : recent_best, 'comments':comments})

def blogs(request, query):
    month_ago = datetime.date.today() - datetime.timedelta(days = 30)
    options = ['trending', 'popular']
    q = query.lower()
    context = {}
    if q in options:
        if q == options[0]:
            context ={
                'posts' : Post.objects.filter(time_upload__gte = month_ago).order_by('-read'),
                'title' : "Trending posts",
                'side_title' : "Popular posts",
                'side_posts' : Post.objects.filter(publish = True),
                'option' : 0,
            }
        elif q == options[1]:
            context ={
                'title' : "Popular posts",
                'posts' : Post.objects.filter(publish = True),
                'side_title' : "Trending posts",
                'side_posts' : Post.objects.filter(time_upload__gte = month_ago).order_by('-read'),
                'option' : 1,
            }
        else:
            pass
    return render(request, 'blogs.html', context)

    
def contact(request):
    if request.method == 'POST':
        name = f"{request.POST.get('fname')} {request.POST.get('lname')}"
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        contact_info = Contact(name =name, email = email, phone = phone, message = message)
        contact_info.save()
    return render(request, 'contact.html')

@login_required(login_url='/accounts/login/')
def create_post(request):
    if request.method == 'POST':
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid:
            post = form.save(commit=False)
            post.author = request.user.author
            post.save()
        return redirect('home')
    else:
        form = CreateForm()
    return render(request, 'create_post.html', {'form': form})
    