
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import ListView

from folha.core.forms import MatriculaListForm
from folha.core.models import Orgao, Matricula, ContraCheque


#home = login_required(ListView.as_view(template_name='index.html', model=Orgao))
from folha.core.tables import ContraChequeTable


@login_required
def home (request):

    # Contra-Cheques
    if request.method == 'POST':
        # Busca os dados fo form
        form = MatriculaListForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            matricula = data['matricula']
            exercicio = data['exercicio']

        qs = ContraCheque.objects.contracheques_by_matricula(matricula, exercicio)
    else:
        # Matrícula
        matriculas = Matricula.objects.matriculas_by_user(request.user)
        form = MatriculaListForm()
        form.fields["matricula"].queryset = matriculas

        #Queryset vazio
        qs = ContraCheque.objects.none()



    table = ContraChequeTable(qs)
    context = {'form': form, 'table':table}

    return render(request, 'index.html', context)
