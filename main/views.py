from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse_lazy


def index(request):

    return redirect(reverse_lazy("accounts:login"))

def dashboard(request):

    return render(request, "main/dashboard.html")