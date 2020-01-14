from django.shortcuts import render, redirect
from fund import models
# Create your views here.
from fund.forms import FbFundForm


def list(request):
    funds = models.FbFunding.objects.all()

    return render(request, "fund/list.html", context={"funds": funds})

def add_fund(request):
    form = FbFundForm(request.POST, request.FILES)
    if request.method == "POST":
        print(request.POST)
        print(form.errors, "jkfjsdfjdksfksn")
        if form.is_valid():
            form.save()
            return redirect("fund:list")
    return render(request, "fund/add-fund.html", context={"form": form})

def view(request, **kwargs):
    fund = models.FbFunding.objects.get(pk=kwargs.get("id"))
    return render(request, "fund/details.html", context={"fund": fund})