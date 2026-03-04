from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import RegisterForm, LoginForm

from realestate.globals import logger
from users.repositories import user_repo

# 4 Authentication & authorization
def register_get(req: HttpRequest):
    form = RegisterForm()

    # 5 Security logging
    logger.info("User 'guest' accessed: Register page.")
    return render(req, "auth/register.html", {"form": form})

def register_post(req: HttpRequest):
    form = RegisterForm(req.POST)

    # 2 Input validation & sanitization
    if not form.is_valid():
        # 5 Security logging
        logger.error("Registration failed due to validation errors.")
        return render(req, "auth/register.html", {"form": form})

    if user_repo.is_registered(form.cleaned_data["email"]):
        messages.error(req, "Korisnik sa ovom imejl adresom već postoji. Pokušaj ponovo.")

        # 5 Security logging
        logger.error("Registration failed because an user with the email address already exists.")
        return render(req, "auth/register.html", {"form": form})
    
    user = user_repo.create(form.cleaned_data)
    login(req, user)
    
    # 5 Security logging
    logger.info("User registered successfully.")
    return redirect("listing-list")

def login_post(req: HttpRequest):
    form = LoginForm(req, req.POST)

    # 2 Input validation & sanitization
    if form.is_valid():
        data = form.cleaned_data
        
        if user_repo.is_registered(data["username"]):
            user = authenticate(req, username=data["username"], password=data["password"])

            if user is not None:
                login(req, user)

                # 5 Security logging
                logger.info("User logged in successfully.")
                return redirect(reverse("listing-list"))
            
            messages.error(req, "Ovi kredencijali ne postoje. Pokušaj ponovo.")

            # 5 Security logging
            logger.error("Login failed because an user with these credentials does not exist.")
            return redirect(reverse("login"))

        messages.error(req, "Korisnik sa ovom imejl adresom ne postoji. Pokušaj ponovo.")

        # 5 Security logging
        logger.error("Login failed because an user with this email address does not exist.")
        return redirect(reverse("login"))
    
    # 5 Security logging
    logger.error("Login failed due to validation errors.")
    return render(req, "auth/login.html", {"form": form})

def login_get(req: HttpRequest):
    form = LoginForm()

    # 5 Security logging
    logger.info("User 'guest' accessed: Login page.")
    return render(req, "auth/login.html", {"form": form})

def register(req: HttpRequest):
    return register_post(req) if req.method == "POST" else register_get(req)
        
def login2(req: HttpRequest):
    return login_post(req) if req.method == "POST" else login_get(req)

@login_required
def logout2(request):
    # 3 Authentication and authorization (role-based)
    logout(request)
    return redirect("login")
