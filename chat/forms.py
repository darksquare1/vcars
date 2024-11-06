from django import forms
from chat.models import ChatGroup


class ChatGroupForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ('name',)
        widgets = {'name': forms.TextInput(attrs={'class ': 'form-control-mb', 'id':'name-field'})}
        labels = {'name': 'Название чата'}
