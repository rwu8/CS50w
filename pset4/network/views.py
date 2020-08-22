import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import datetime
from .models import User, UserFollowing, Post, Comment, Like


def comment_view(request, post_id):
    post = Post.objects.get(pk=post_id)

    # delete user comment
    if "remove_comment" in request.POST:
        if request.POST["remove_comment"]:
            comment = Comment.objects.get(pk=request.POST['comment_id'])
            comment.delete()

            comments = Comment.objects.filter(post=post)
            return render(request, "network/comment.html", {
                'post': post,
                'comments': comments
            })

    try:
        comments = Comment.objects.filter(post=post)
    except:
        comments = []
    
    if request.method == "POST":
        comment_body = request.POST["post"]
        new_comment = Comment(comment=comment_body, user=request.user, post=post)
        new_comment.save()
    
    comments = Comment.objects.filter(post=post)
    return render(request, "network/comment.html", {
        'post': post,
        'comments': comments
    })



def following_view(request):
    # TODO
    user = User.objects.get(pk=request.user.id)
    followers = user.followers.all()
    posts = []
    
    if len(followers) > 0:
        for user in followers:
            posts.append(Post.objects.filter(user=user.user_id))
        posts = posts[0]
        p = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number)
    return render(request, "network/following.html", {
            "posts": page_obj,
            "pages": p
        })


def index(request):
    if request.method == "POST":
        post = Post(user=request.user, body=request.POST["post"], comments=None)
        post.save()
    posts = Post.objects.all().order_by('-timestamp')
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    return render(request, "network/index.html", {
        "posts": page_obj,
        "pages": p
    })


def like_view(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(pk=post_id)
        # Query for requested Like
        try:
            like = Like.objects.get(user=request.user, post=post)
            print(like)
            # The Like exists aready, check if currently liking post
            if like and like.currently_liked == True:
                like.currently_liked = False
                post.total_likes -= 1
                post.user_likes.remove(request.user)
                post.save()           
                like.save()
                # Respond with success status
                return HttpResponse(status=204)
            elif like and like.currently_liked == False:
                print('else', like)
                like.currently_liked = True
                post.total_likes += 1
                post.user_likes.add(request.user)
                post.save()
                like.save()
                # Respond with success status
                return HttpResponse(status=204)
        
        # The Like is new
        except Like.DoesNotExist:
            new_like = Like(user=request.user, post=post, currently_liked=True)
            # print(new_like)
            post.total_likes += 1
            post.user_likes.add(request.user)
            post.save()
            new_like.save()
            # Respond with success status
            return HttpResponse(status=204)
    
    if request.method == "GET":
        print("GET METHOD")
        post = Post.objects.get(pk=post_id)
        print("NUMBER OF LIKES", post.total_likes)
        return JsonResponse(post.total_likes, safe=False)


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
    # delete user post
    if "remove_post" in request.POST:
        if request.POST["remove_post"]:
            post = Post.objects.get(user=request.user, pk=post_id)
            post.delete()
            return HttpResponseRedirect(reverse("index"))

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
    try:
        requesting_user = User.objects.get(pk=request.user.id)
    except:
        requesting_user = None
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