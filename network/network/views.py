from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from .models import User, Post, Profile


def index(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    return render(request, "network/index.html", {'posts': page_posts})


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@require_POST
@login_required(login_url='/login')
def create(request):
    content = request.POST["content"]
    if content:
        Post.objects.create(user=request.user,
                            content=content)

    return HttpResponseRedirect(reverse('index'))


@require_POST
@login_required(login_url='/login')
def edit_post(request):
    content = request.POST["content"]
    post_id = request.POST.get('post_id')
    if content:
        post = get_object_or_404(Post, id=post_id)
        if post.user == request.user:
            post.content = content.strip()
            post.save()

    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='/login')
def profile(request, user_id):
    p_user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user=p_user)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)
    followers = p_user.follower.all()
    followings = p_user.following.all()
    context = {
        'followers': followers,
        'followings': followings,
        'profile_user': p_user,
        'posts': page_posts,
        'has_follower': followers.filter(follower__id=request.user.id).exists(),
    }

    return render(request, "network/profile.html", context)


@login_required(login_url='/login')
def following(request):
    current_user = request.user
    following_users = Profile.objects.filter(follower=current_user).values('following_id')
    posts = Post.objects.filter(user__in=following_users)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)

    return render(request, 'network/following.html', { 'posts': page_posts })


@login_required(login_url='/login')
def follow(request, user_id):
    f_user = get_object_or_404(User, id=user_id)
    Profile.objects.create(follower=request.user, following=f_user)

    return HttpResponseRedirect(reverse('profile', kwargs={'user_id':user_id}))


@login_required(login_url='/login')
def unfollow(request, user_id):
    uf_user = get_object_or_404(User, id=user_id)
    Profile.objects.filter(follower=request.user, following=uf_user).delete()

    return HttpResponseRedirect(reverse('profile', kwargs={'user_id':user_id}))


@login_required(login_url='/login')
def like_post(request, post_id):
    user = request.user
    current_post = Post.objects.get(id=post_id)
    if current_post.like.filter(id=user.id).exists():
        current_post.like.remove(user)
    else:
        current_post.like.add(user)

    return JsonResponse({'likes': current_post.like.count(), "status": 201})
