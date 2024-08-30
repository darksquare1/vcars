from django import forms
from taggit.forms import TagField
from .models import Comment, Pic


class CommentForm(forms.ModelForm):
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={"class": "form-control mb-1", }))
    body = forms.CharField(label='Комментарий', widget=forms.TextInput(attrs={"class": "form-control mb-1", }))

    class Meta:
        model = Comment
        fields = ['name', 'body']


class PicForm(forms.ModelForm):
    tags = TagField(label='Тэги', required=True,
                           widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Тэги через запятую'}))
    name = forms.CharField(label='Название', required=True,
                           widget=forms.TextInput(attrs={"class": "form-control"}))
    pic = forms.ImageField(label='Картинка', required=True, widget=forms.FileInput(
        attrs={'class': 'form-control', 'id': 'customFile'}
    ))
    body = forms.CharField(label='Описание', required=True,
                           widget=forms.Textarea(attrs={"class": "form-control",
                                                        'placeholder': 'Напишите что нибудь интересное о вашей картинке'}))

    class Meta:
        model = Pic
        fields = ['tags', 'name', 'pic', 'body']
