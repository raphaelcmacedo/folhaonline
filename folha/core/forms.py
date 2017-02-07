import datetime

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from folha.core.models import Matricula, Orgao


class MatriculaListForm(forms.Form):
     exercicio = forms.IntegerField(initial=datetime.datetime.now().year)
     matricula = forms.ModelChoiceField(queryset=Matricula.objects.all())


class ContraChequeUploadForm(forms.Form):
     formato_choices =(
          ('SAPITUR', 'Sapitur'),
          ('CAMBUCI', 'Cambuci'),
     )

     action_choices = (
         ('IMPORT', 'Importar contra cheque'),
         ('REGISTER', 'Cadastrar usuários'),
     )

     orgao = forms.ModelChoiceField(label="Orgão",queryset=Orgao.objects.all())
     formato = forms.ChoiceField(formato_choices)
     action = forms.ChoiceField(action_choices, label="Ação")
     file = forms.FileField(label="Arquivo", widget=forms.ClearableFileInput(attrs={'multiple': True}))

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Endereço de e-mail já utilizado para outro usuário')
        return email

class UserListForm(forms.Form):
    orgao = forms.ModelChoiceField(label="Orgão", queryset=Orgao.objects.all())
    search = forms.CharField(label="Filtro", max_length=100, required=False)

