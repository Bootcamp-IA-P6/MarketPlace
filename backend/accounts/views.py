from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

def login_view(request):
    form = LoginForm(request.POST or None)
    message = ""

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("main_page")
            else:
                message = "Username or password is incorrect"

    return render(request, "accounts/login.html", {
        "form": form,
        "message": message
    })


def logout_view(request):
    logout(request)
    return redirect("login")
