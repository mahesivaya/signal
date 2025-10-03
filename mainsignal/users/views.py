from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.conf import settings
from .models import PasswordReset
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import logging
logger = logging.getLogger('django')

# Create your views here.
def logintest(request):
    """
    Render the login page.
    """
    return render(request, "logintest.html", {"message": "Welcome to the login page"})


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user_data_has_error = False

        if User.objects.filter(username=username).exists():
            user_data_has_error = True
            messages.error(request, "Username already exists")

        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, "Email already exists")

        if len(password) < 5:
            user_data_has_error = True
            messages.error(request, "Password must be at least 5 characters")

        if user_data_has_error:
            return redirect("register")
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            messages.success(request, "Account created. Login now")
            return redirect("login")

    return render(request, "register.html")

def loginView(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid login credentials")
            return redirect("login")

    return render(request, "login.html")


@login_required
def home(request):

    return render(request, "home.html", {"message": "Welcome to the login page"})


def userpage(request, username):
    return JsonResponse({'message': f'Welcome, {username}!'})


def logout(request):

    return redirect("login")


def forgotPassword(request):

    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse(
                "reset-password", kwargs={"reset_id": new_password_reset.reset_id}
            )

            full_password_reset_url = (
                f"{request.scheme}://{request.get_host()}{password_reset_url}"
            )

            email_body = f"Reset your password using the link below:\n\n\n{full_password_reset_url}"

            email_message = EmailMessage(
                "Reset your password", email_body, settings.EMAIL_HOST_USER, [email]
            )

            email_message.fail_silently = True
            email_message.send()

            return redirect("password-reset-sent", reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect("forgot-password")

    return render(request, "forgot_password.html")


class LogIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        logger.info(f"[{request.method}] Request from IP: {ip} to {request.path}")
        return self.get_response(request)
