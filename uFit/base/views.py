from typing import AsyncGenerator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Profile, Event
from .forms import PostForm, ProfileForm, EventForm
from django.http import Http404, HttpRequest, StreamingHttpResponse, HttpResponse, JsonResponse, HttpResponseRedirect
from . import models
import asyncio
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
import random
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils.timezone import now
""" from .models import Post
 """
# Create your views here.
def lobby(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        username = request.POST.get("username")
        if username:
            request.session["username"] = username
        else:
            names = [
                "Horatio",
                "Benvolio",
                "Mercutio",
                "Lysander",
                "Demetrius",
                "Sebastian",
                "Orsino",
                "Malvolio",
                "Hero",
                "Bianca",
                "Gratiano",
                "Feste",
                "Antonio",
                "Lucius",
                "Puck",
                "Lucio",
                "Goneril",
                "Edgar",
                "Edmund",
                "Oswald",
            ]
            request.session["username"] = (
                f"{random.choice(names)}-{hash(datetime.now().timestamp())}"
            )

        return redirect("chatpage")
    else:
        return render(request, "base/lobby.html")


def chatpage(request: HttpRequest) -> HttpResponse:
    if not request.session.get("username"):
        return redirect("home")
    return render(request, "base/chatpage.html")


def create_message(request: HttpRequest) -> HttpResponse:
    content = request.POST.get("content")
    username = request.session.get("username")

    if not username:
        return HttpResponse(status=403)
    author, _ = models.Author.objects.get_or_create(name=username)

    if content:
        models.Message.objects.create(author=author, content=content)
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=200)


async def stream_chat_messages(request: HttpRequest) -> StreamingHttpResponse:
    """
    Streams chat messages to the client as we create messages.
    """

    async def event_stream():
        """
        We use this function to send a continuous stream of data
        to the connected clients.
        """
        async for message in get_existing_messages():
            yield message

        last_id = await get_last_message_id()

        # Continuously check for new messages
        while True:
            new_messages = (
                models.Message.objects.filter(id__gt=last_id)
                .order_by("created_at")
                .values("id", "author__name", "content")
            )
            async for message in new_messages:
                yield f"data: {json.dumps(message)}\n\n"
                last_id = message["id"]
            await asyncio.sleep(
                0.1
            )  # Adjust sleep time as needed to reduce db queries.

    async def get_existing_messages() -> AsyncGenerator:
        messages = (
            models.Message.objects.all()
            .order_by("created_at")
            .values("id", "author__name", "content")
        )
        async for message in messages:
            yield f"data: {json.dumps(message)}\n\n"

    async def get_last_message_id() -> int:
        last_message = await models.Message.objects.all().alast()
        return last_message.id if last_message else 0

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")


def welcomePage(request: HttpRequest):
    return render(request, "base/welcome.html")


def privacyPage(request):
    return render(request, "base/privacy.html")

@login_required
def homePage(request):
    query = request.GET.get("q", "")

    # Filter posts based on the search query
    posts = Post.objects.filter(
        Q(title__icontains=query) | 
        Q(body__icontains=query) | 
        Q(host__username__icontains=query) |
        Q(host__profile__role__icontains=query)
    ) if query else Post.objects.all()

    # Get upcoming events
    events = Event.objects.filter(date__gte=now().date()).order_by('date', 'time')

    # Paginate posts and events
    post_paginator = Paginator(posts, 10)
    post_page_number = request.GET.get('page')
    posts = post_paginator.get_page(post_page_number)

    event_paginator = Paginator(events, 5)
    event_page_number = request.GET.get('event_page')
    events = event_paginator.get_page(event_page_number)

    context = {"posts": posts, "events": events}
    return render(request, "base/home.html", context)

# uFit/base/views.py

from django.shortcuts import render, redirect
from .models import Post
from django.contrib.auth.decorators import login_required

@login_required
def postpage(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        print(form.is_valid)
        if form.is_valid():
            print("FOrm is vaLIDDD")
            post = form.save(commit=False)
            post.host = request.user
            post.created = datetime.now()
            post.save()
            return redirect('home')
    else:
        print("thfiaohefhaofo")
        form = PostForm()
    context = {"form" : form}
    return render(request, 'base/postpage.html', context)

def profilepage(request, pk):
    user = get_object_or_404(User, pk=pk)
    posts = Post.objects.filter(host=user)
    context = {"user": user, "posts": posts}
    return render(request, "base/profilepage.html", context)


def login_page(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            request.session["username"] = username
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                return redirect(
                    "home"
                )  # Redirect to the home page after successful login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = AuthenticationForm()  # Display an empty login form

    return render(request, "base/loginpage.html", {"form": form})


def registration_page(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in immediately after registration
            messages.success(
                request, "Registration successful!"
            )  # Optional success message
            return redirect(
                "home"
            )  # Redirect to home page after successful registration
        else:
            messages.error(request, "There was an error with your registration.")
    else:
        form = UserCreationForm()  # Display an empty form

    return render(request, "base/registrationpage.html", {"form": form})

@csrf_exempt
@login_required
def search_posts(request):
    query = request.GET.get("q", "")
    if query:
        posts = Post.objects.filter(
            Q(host__username__icontains=query) | 
            Q(title__icontains=query) | 
            Q(body__icontains=query)
        ).values("host__username", "title", "body")
    else:
        posts = []

    return JsonResponse(list(posts), safe=False)


def updatePost(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/home/")  # Redirect to the home page
    else:
        form = PostForm(instance=post)
    return render(request, "base/updatepost.html", {"form": form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Ensure the logged-in user is the owner of the post
    if post.host != request.user:
        raise Http404("You do not have permission to delete this post.")
    if request.method == "POST":
        post.delete()
        return redirect('home')  # Redirect to the home page after deletion

    return render(request, 'base/delete_post.html', {'post': post})

@login_required
def update_profile(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise Http404("User does not exist")

    if user != request.user and not request.user.is_staff:
        raise Http404("You do not have permission to update this user's profile")

    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profilepage", pk=request.user.pk)
    else:
        form = ProfileForm(instance=profile)

    return render(request, "base/update-profile.html", {"form": form})
   

@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('home')
    else:
        form = EventForm()

    return render(request, 'base/add_event.html', {'form': form})

