from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    name = forms.CharField(label='Имя',widget=forms.TextInput(attrs={"class": "form-control mb-1",}))
    body = forms.CharField(label='Комментарий', widget=forms.TextInput(attrs={"class": "form-control mb-1",}))

    class Meta:
        model = Comment
        fields = ['name', 'body']
