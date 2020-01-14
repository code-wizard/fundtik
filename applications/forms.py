from django.forms import ModelForm

from applications import models


class FbApplicationForm(ModelForm):

    class Meta:
        model = models.FbApplication
        fields = "__all__"