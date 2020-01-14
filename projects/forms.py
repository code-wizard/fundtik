from django.forms import ModelForm

from projects.models import FbProjects, FbMileStones


class FbProjectForm(ModelForm):

    class Meta:
        model = FbProjects
        fields ="__all__"


class FbMileStonesForm(ModelForm):

    class Meta:
        model = FbMileStones
        fields ="__all__"
