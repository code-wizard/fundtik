from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model

from projects.models import FbProjects, FbMileStones
from fund.models import FbFunding

FbUser = get_user_model()


class FbProjectForm(ModelForm):
    funding = forms.ModelMultipleChoiceField(
        queryset=FbFunding.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select one or more funding sources for this project"
    )
    
    class Meta:
        model = FbProjects
        fields = ['name', 'category', 'start_date', 'end_date', 'description', 'budget', 'file', 'funding']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'category': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('', '--Select Category--'),
                ('Agriculture', 'Agriculture'),
                ('Infrastructure', 'Infrastructure'),
                ('Green Initiative', 'Green Initiative'),
                ('Education', 'Education'),
                ('Healthcare', 'Healthcare'),
                ('Technology', 'Technology'),
            ]),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your project...'}),
            'budget': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'file': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("End date must be after start date.")
        
        return cleaned_data
    
    def clean_budget(self):
        budget = self.cleaned_data.get('budget')
        if budget is not None and budget < 0:
            raise forms.ValidationError("Budget cannot be negative.")
        return budget


class FbMileStonesForm(ModelForm):
    assignee = forms.ModelChoiceField(
        queryset=FbUser.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select user to assign this milestone to"
    )

    class Meta:
        model = FbMileStones
        fields = ['name', 'due_date', 'description', 'reminder', 'assignee', 'file']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter milestone name'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe the milestone...'}),
            'reminder': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'Days before due date'}),
            'file': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
