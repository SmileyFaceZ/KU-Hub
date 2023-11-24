from django import forms
from kuhub.models import Tags, Subject, Profile, PostComments, PostReport


class PostForm(forms.Form):
    TAG_CHOICES = [
        (tag.tag_text, tag.tag_text) for tag in Tags.objects.all()
    ]

    SUBJECT_CHOICES = [
        (subject.course_code, subject.course_code + " " + subject.name_eng)
        for subject in Subject.objects.all()
    ]

    tag_name = forms.ChoiceField(
        choices=TAG_CHOICES,
        label='Tags',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        label='Subjects',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    review = forms.CharField(
        widget=forms.Textarea(attrs={'cols': 100, 'rows': 3}),
        label='Review',
        required=True
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['biography', 'display_photo']


class GroupForm(forms.Form):
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
    class Meta:
        model = PostComments
        fields = ['comment']


class ReportForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea)

