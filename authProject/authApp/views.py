from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import RegisterForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(
                username=username,
                password=password,
            )
            login(request, user)
            return redirect("home")
        else:
            form = RegisterForm()
            context = {
                "form": form,
            }
            return render(
                request,
                "authApp/accounts/register.html",
                context
            )

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user is not None:
            login(request, user)
            next_url = request.POST.get("next") or request.GET.get("next") or "home"
            redirect(next_url)
        else:
            error_message = "Invalid Credentials"
    return render(
        request,
        "authApp/accounts/login.html",
        {"error": error_message},
    )
        
        
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    else:
        return redirect("home")

@login_required
def home(request):
    return render(
        request,
        "authApp/home/home.html",
    )

class ProtectedView(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "redirect_to"
    
    def get(self, request):
        return render(
            request,
            "authApp/registration/protected.html",
        )


