from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
def welcomePage(request):
    return render(request, "base/welcome.html", {})


def privacyPage(request):
    return render(request, "base/privacy.html")
    return render(request, "base/privacy.html")

@login_required
def homePage(request):
    return render(request, "base/home.html")


def registration_page(request):
    return render(request, "base/registrationpage.html")


def chatpage(request):
    return render(request, "base/chatpage.html")


def postpage(request):
    return render(request, "base/postpage.html")


def profilepage(request):
    return render(request, "base/profilepage.html")


def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log the user in
                next_url = request.GET.get('next', 'home')  # Get the next URL from the request
                return redirect(next_url)  # Redirect to the home page after successful login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = AuthenticationForm()  # Display an empty login form

    return render(request, 'base/loginpage.html', {'form': form})

def registration_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in immediately after registration
            messages.success(request, "Registration successful!")  # Optional success message
            return redirect('home')  # Redirect to home page after successful registration
        else:
            messages.error(request, "There was an error with your registration.")
    else:
        form = UserCreationForm()  # Display an empty form

    return render(request, 'base/registrationpage.html', {'form': form})

