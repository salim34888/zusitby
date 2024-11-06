from django import forms
from courses.models import Course
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        super(CourseEnrollForm, self).__init__(*args, **kwargs)
        self.fields['course'].queryset = Course.objects.all()


class AnswerForm(forms.Form):
    answer = forms.CharField(label='Ваш ответ', max_length=255)
    question_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
        self.fields['answer'].label = f'Ваш ответ на вопрос: {self.question.text}' if self.question else 'Ваш ответ'
        self.fields['question_id'].initial = self.question.id


class CodeForm(forms.Form):
    code = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Введите ваш код здесь',
            'rows': 10,
            'cols': 60
        }),
        label="Введите код"
    )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']

