from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from questions.forms import FbQuestionForm
from questions.models import FbQuestions


@login_required()
def list(request):
    form = FbQuestionForm(initial={})
    questions = FbQuestions.objects.all()
    if request.method == "POST":
        data = request.POST.copy()
        data["created_by"] = request.user.uuid
        form = FbQuestionForm(data, request.FILES)
        if form.is_valid():
            print(form.errors)

            form.save()

            form = FbQuestionForm()
        print(form.errors)
    return render(request, "questions/list.html", {"form": form, "questions": questions})