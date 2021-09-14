from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.db.models import Max
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import User, News, Category, Comment
from .forms import NewsForm


def index(request):
    last_four_hot_news = News.objects.filter(is_hot_news=True).order_by('-last_modified')
    news = News.objects.filter(is_active=True).order_by('-last_modified')
    paginator = Paginator(news, 10)
    news_number = request.GET.get('page')
    page_news = paginator.get_page(news_number)    
    return render(request, "news/index.html", {
        "hot_news": last_four_hot_news[:4],
        "all_news": page_news,
        "categories": Category.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "news/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "news/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "news/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "news/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "news/register.html")


def europe_news(request):
    hot_news_by_category = News.objects.filter(is_hot_news=True, is_active=True, category__title="Europe").order_by('-last_modified')
    news = News.objects.filter(is_active=True, category__title="Europe").order_by('-last_modified')
    paginator = Paginator(news, 10)
    news_number = request.GET.get('page')
    page_news = paginator.get_page(news_number)  

    return render(request, "news/index.html", {
        "hot_news": hot_news_by_category[:4],
        "all_news": page_news,
        "categories": Category.objects.all()
    })  


def world_news(request):
    hot_news_by_category = News.objects.filter(is_hot_news=True, is_active=True, category__title="World").order_by('-last_modified')
    news = News.objects.filter(is_active=True, category__title="World").order_by('-last_modified')
    paginator = Paginator(news, 10)
    news_number = request.GET.get('page')
    page_news = paginator.get_page(news_number)  

    return render(request, "news/index.html", {
        "hot_news": hot_news_by_category[:4],
        "all_news": page_news,
        "categories": Category.objects.all()
    }) 


def sport_news(request):
    hot_news_by_category = News.objects.filter(is_hot_news=True, is_active=True, category__title="Sport").order_by('-last_modified')
    news = News.objects.filter(is_active=True, category__title="Sport").order_by('-last_modified')
    paginator = Paginator(news, 10)
    news_number = request.GET.get('page')
    page_news = paginator.get_page(news_number)  

    return render(request, "news/index.html", {
        "hot_news": hot_news_by_category[:4],
        "all_news": page_news,
        "categories": Category.objects.all()
    }) 


def category_news(request, id):
    hot_news_by_category = News.objects.filter(is_hot_news=True, is_active=True, category__id=id).order_by('-last_modified')
    news = News.objects.filter(is_active=True, category__id=id).order_by('-last_modified')
    paginator = Paginator(news, 10)
    news_number = request.GET.get('page')
    page_news = paginator.get_page(news_number)  

    return render(request, "news/index.html", {
        "hot_news": hot_news_by_category[:4],
        "all_news": page_news,
        "categories": Category.objects.all()
    })    


def categories(request):
    return render(request, "news/categories.html", { "categories": Category.objects.all() })


def news_detail(request, slug):
    user = request.user
    news = News.objects.get(slug=slug)
    return render(request, "news/news_detail.html", {
        "news": news,
        "categories": Category.objects.filter(news_category=news.id),
        "comments": Comment.objects.filter(news=news.id),
        "owner": news.user == user
    })    


@login_required(login_url='/login')
def create(request):
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES or None)
        if form.is_valid():
            news = News.objects.create(user=request.user,
                                       title=form.cleaned_data["title"],
                                       content=form.cleaned_data["content"],
                                       slug=form.cleaned_data["slug"],
                                       image=form.cleaned_data["image"],
                                       is_active=form.cleaned_data["is_active"],
                                       is_hot_news=form.cleaned_data["is_hot_news"])
            categories_ids = dict(request.POST)['categories']
            news.category.add(*categories_ids)
    
        return HttpResponseRedirect(reverse('index'))

    else:
        form = NewsForm()
        return render(request, "news/create.html", {
            "form": form,
            "categories": Category.objects.all()
        })


@login_required(login_url='/login')
def edit_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES or None)
        if form.is_valid():
            news.title = form.cleaned_data["title"]
            news.content = form.cleaned_data["content"]
            news.slug = form.cleaned_data["slug"]
            news.is_active = form.cleaned_data["is_active"]
            news.is_hot_news = form.cleaned_data["is_hot_news"]
            if form.cleaned_data["image"]:
                news.image = form.cleaned_data["image"]
            categories_ids = dict(request.POST)['categories']
            news.category.clear()
            news.category.add(*categories_ids)
            news.save()
            return HttpResponseRedirect(reverse('news_detail', kwargs={'slug': news.slug}))
    else:
        return render(request, "news/edit_news.html", { 
            "news": news,
            "categories": Category.objects.all()
        })


def edit(request, title):
    if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            util.save_entry(title, content)
            return render(request, "encyclopedia/detail.html", {
                "content": content, "title": title
            })
    else:
        return render(request, "encyclopedia/edit.html", {
            "content": util.get_entry(title), "title": title
        })


@require_POST
@login_required(login_url='/login')
def create_comment(request, news_id):
    user = request.user
    news = News.objects.get(id=news_id)
    comment = request.POST["comment"]
    if comment:
        Comment.objects.create(user=user, news=news, comment=comment)
    return HttpResponseRedirect(reverse('news_detail', kwargs={'slug': news.slug}))


@login_required(login_url='/login')
def bookmark_news(request, news_id):
    user = request.user
    current_news = News.objects.get(id=news_id)
    if current_news.bookmarks.filter(id=user.id).exists():
        current_news.bookmarks.remove(user)
        return JsonResponse({'bookmarked': False, "status": 201})
    else:
        current_news.bookmarks.add(user)
        return JsonResponse({'bookmarked': True, "status": 201})


@login_required(login_url='/login')
def bookmarked_news(request, user_id):
    b_user = get_object_or_404(User, id=user_id)
    bookmarked_news = b_user.news_bookmarks.all().order_by('-last_modified')
    paginator = Paginator(bookmarked_news, 10)
    news_number = request.GET.get('page')
    page_news = paginator.get_page(news_number)    
    return render(request, "news/bookmarked_news.html", { "all_news": page_news, "categories": Category.objects.all() })    


def profile(request, user_id):
    p_user = get_object_or_404(User, id=user_id)
    news = News.objects.filter(user=p_user).order_by('-last_modified')
    paginator = Paginator(news, 10)
    page_number = request.GET.get('page')
    page_news = paginator.get_page(page_number)
    context = {
        'profile_user': p_user,
        'all_news': page_news
    }
    return render(request, "news/profile.html", context)


def search_news(request):
    query = request.GET.get('q')
    results = News.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-last_modified')
    paginator = Paginator(results, 10)
    news_number = request.GET.get('page')
    page_news = paginator.get_page(news_number)      
    return render(request, "news/index.html", {
        "all_news": page_news,
        "query": query,
        "categories": Category.objects.all()
    })
