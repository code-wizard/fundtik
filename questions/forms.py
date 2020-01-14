from django.forms import ModelForm

from questions import models


class FbQuestionForm(ModelForm):

    class Meta:
        model = models.FbQuestions
        fields = "__all__"