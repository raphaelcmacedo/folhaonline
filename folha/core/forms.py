import datetime

from django import forms
from django.core.exceptions import ValidationError

from folha.core.models import Matricula


class MatriculaListForm(forms.Form):
     exercicio = forms.IntegerField(initial=datetime.datetime.now().year)
     matricula = forms.ModelChoiceField(queryset=Matricula.objects.all())

