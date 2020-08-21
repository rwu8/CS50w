import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import datetime
from .models import User, UserFollowing, Post, Comment, Like


def following_view(request):
    # TODO
    user = User.objects.get(pk=request.user.id)
    followers = user.followers.all()
    posts = []
    # print('length: ', len(followers))
    if len(followers) > 0:
        for user in followers:
            posts.append(Post.objects.filter(user=user.user_id))
        posts = posts[0]
    

    return render(request, "network/following.html", {
            "posts": posts
        })

def index(request):
    if request.method == "POST":
        post = Post(user=request.user, body=request.POST["post"], comments=None, likes=None)
        post.save()
    posts = Post.objects.all().order_by('-timestamp')
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    return render(request, "network/index.html", {
        "posts": page_obj,
        "pages": p
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def post_view(request, post_id):
    # print(request.POST)
    # Query for requested post
    try:
        post = Post.objects.get(user=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    # Update the posts body and timestamp 
    if request.method == "PUT":
        data = json.loads(request.body)
        post.body = data['body']
        post.timestamp =  '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        post.save()
        return HttpResponse(status=204)


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


def user_view(request, user_id):
    # TODO
    requesting_user = User.objects.get(pk=request.user.id)
    user = User.objects.get(pk=user_id)

    if request.method == "POST":
        if 'add_follow' in request.POST:
            follower = UserFollowing(user_id=user, following_user_id=requesting_user)
            follower.save()

        if 'remove_follow' in request.POST:
            follow = UserFollowing.objects.get(user_id=user, following_user_id=requesting_user)
            follow.delete()
    
    followers = user.following.all()
    following = user.followers.all()

    try:
        if UserFollowing.objects.get(user_id=user, following_user_id=requesting_user):
            is_following = True
    except:
        is_following = False

    # display posts in reverse chronological order
    user_posts = Post.objects.filter(user=user).order_by('-timestamp')
    p = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    return render(request, "network/user.html", {
        "user": user,
        "following": following,
        "followers": followers,
        "posts": page_obj,
        "pages": p,
        "requesting_user": requesting_user,
        "is_following": is_following
    })