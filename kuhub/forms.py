"""This module contains various forms used throughout the application."""
from django import forms
from kuhub.models import Tags, Subject, Profile, PostComments


class PostForm(forms.Form):
    """From for creating or editing a post."""

    tag_name = forms.ChoiceField(
        label='Tags',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    subject = forms.ChoiceField(
        label='Subjects',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    review = forms.CharField(
        widget=forms.Textarea(),
        label='Review',
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['tag_name'].choices = [(tag.tag_text, tag.tag_text) for tag in Tags.objects.all()]
        self.fields['subject'].choices = [
            (subject.course_code, subject.course_code + " " + subject.name_eng)
            for subject in Subject.objects.all()
        ]


class ProfileForm(forms.ModelForm):
    """Form is used for creating and editing user profiles."""

    class Meta:
        model = Profile
        fields = ['biography', 'display_photo']


class GroupForm(forms.Form):
    """Form for creating or managing a group."""

    name = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}),
        label='Group name:',
        required=True
    )
    tag_name = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 70, 'rows': 1}),
        label='Tags :',
        required=False
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 100, 'rows': 3}),
        label='Description',
        required=False
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Password',
        required=False
    )
    password_2 = forms.CharField(
        widget=forms.PasswordInput,
        label='Password',
        required=False
    )


class EventForm(forms.Form):
    """Form for creating or editing events."""

    start_time = forms.DateTimeField(
        widget=forms.TextInput(attrs={'type': 'datetime-local'}),
        label='Start Time',
        required=True
    )
    end_time = forms.DateTimeField(
        widget=forms.TextInput(attrs={'type': 'datetime-local'}),
        label='End Time',
        required=True
    )
    summary = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}),
        label='Event name:',
        required=True
    )
    location = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 50, 'rows': 1}),
        label='Location:',
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 70, 'rows': 2}),
        label='Location:',
        required=True
    )
    is_meeting = forms.BooleanField(
        required=False,
        widget=forms.RadioSelect(choices=[(True, 'Generate meet')]),
        initial=False,
    )



class CommentForm(forms.ModelForm):
    """Form is used for creating comments on posts."""
    class Meta:
        model = PostComments
        fields = ['comment']


class ReportForm(forms.Form):
    """Form for submitting report issues or content."""
    reason = forms.CharField(widget=forms.Textarea)
