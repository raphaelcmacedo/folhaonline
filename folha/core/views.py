from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.views.generic import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models.query_utils import Q


from folha.core.forms import MatriculaListForm, ContraChequeUploadForm
from folha.core.models import Matricula, ContraCheque
from folha.core.services import upload_contra_cheque_file
from folha.settings import DEFAULT_FROM_EMAIL


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

        sucesses = []
        failures = []

        if form.is_valid():

            data = form.cleaned_data
            formato = data['formato']
            orgao = data['orgao']

            for f in files:
                try:
                    contra_cheque = upload_contra_cheque_file(f, orgao, formato)
                    sucesses.append('O arquivo {} foi importado com sucesso.'.format(str(f)))
                except Exception as e:
                    failures.append('O arquivo {} gerou o seguinte erro: {}'.format(str(f), str(e)))

            return render(request, 'contra_cheque/success.html', {'sucesses': sucesses, 'failures': failures})
    else:
        form = ContraChequeUploadForm()
    return render(request, 'contra_cheque/upload.html', {'form': form})
