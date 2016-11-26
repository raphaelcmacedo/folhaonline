import datetime

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from folha.core.models import Matricula, Orgao


class MatriculaListForm(forms.Form):
     exercicio = forms.IntegerField(initial=datetime.datetime.now().year)
     matricula = forms.ModelChoiceField(queryset=Matricula.objects.all())


class ContraChequeUploadForm(forms.Form):
     choices =(
          ('SAPITUR', 'Sapitur'),
     )

     orgao = forms.ModelChoiceField(label="Orgão",queryset=Orgao.objects.all())
     formato = forms.ChoiceField(choices)
     file = forms.FileField(label="Arquivo", widget=forms.ClearableFileInput(attrs={'multiple': True}))

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class UserListForm(forms.Form):
    orgao = forms.ModelChoiceField(label="Orgão", queryset=Orgao.objects.all())
    username = forms.CharField(label="CNPJ", max_length=11, required=False, help_text='Insira somente os números')
