from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from accounts.utils import generate_jwt
from applications.models import FbApplication
from fund.models import FbFunding
from questions.models import FbQuestions


def list(request):
    return redirect("projects:list")


@login_required
def edit(request, **kwargs):
    questions = FbQuestions.objects.all()
    application = get_object_or_404(FbApplication, pk=kwargs.get("id"))
    document = application.funding.document_id
    print(application.funding.document_id)
    token = generate_jwt(request.user, document)
    return render(request, "applications/edit-application.html", {"questions": questions,
                                                                  "document": document,
                                                                  "token": token, })