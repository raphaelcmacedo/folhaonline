from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from folha.core.forms import MatriculaListForm, ContraChequeUploadForm
from folha.core.models import Matricula, ContraCheque


@login_required
def home (request):
    contra_cheques = []

    if request.method == 'POST':
        # Busca os dados fo form
        form = MatriculaListForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            matricula = data['matricula']
            exercicio = data['exercicio']

        contra_cheques = list(ContraCheque.objects.contracheques_by_matricula(matricula, exercicio))
    else:
        # Matrícula
        matriculas = Matricula.objects.matriculas_by_user(request.user)
        form = MatriculaListForm()
        form.fields["matricula"].queryset = matriculas

    context = {'form': form, 'contra_cheques':contra_cheques}

    return render(request, 'index.html', context)



@login_required
def upload_contra_cheque(request):
    if request.method == 'POST':
        form = ContraChequeUploadForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        if form.is_valid():
            for f in files:
                upload_contra_cheque(f)
            return HttpResponseRedirect('/success/url/')
    else:
        form = ContraChequeUploadForm()
    return render(request, 'contra_cheque/upload.html', {'form': form})