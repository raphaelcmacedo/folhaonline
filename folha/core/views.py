from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AbstractUser
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q

from folha.core.forms import MatriculaListForm, ContraChequeUploadForm, UserForm, UserListForm
from folha.core.models import Matricula, ContraCheque
from folha.core.services import upload_contra_cheque_file, register_matricula
from folha.core.tables import UserTable


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
            action = data['action']
            orgao = data['orgao']

            matriculas_dict = Matricula.objects.matriculas_dict_by_orgao(orgao)

            for f in files:
                try:
                    if action == 'IMPORT':
                        contra_cheque = upload_contra_cheque_file(f, orgao, formato, matriculas_dict)
                        sucesses.append('O arquivo {} foi importado com sucesso.'.format(str(f)))
                    elif action == 'REGISTER':
                        matricula = register_matricula(f, orgao, formato)
                        if matricula is not None:
                            sucesses.append('A matrícula {} foi cadastrada pelo arquivo {}.'.format(str(matricula),str(f)))

                except Exception as e:
                    failures.append('O arquivo {} gerou o seguinte erro: {}'.format(str(f), str(e)))

            return render(request, 'contra_cheque/success.html', {'sucesses': sucesses, 'failures': failures})
    else:
        form = ContraChequeUploadForm()
    return render(request, 'contra_cheque/upload.html', {'form': form})

def edit_user(request, pk = None, template_name="registration/edit_user.html"):
    if pk is None:
        user = request.user
    else:
        user = User.objects.all().filter(pk = pk).first()

    if request.method == "POST":
        form = UserForm(data=request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            url = reverse('home')
            return HttpResponseRedirect(url)
    else:
        form = UserForm(instance=user)

    context = {'form': form}
    return render(request, template_name, context)

@login_required
def list_user (request):

    qs = User.objects.none()

    if request.method == 'POST':
        # Busca os dados do form
        form = UserListForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            orgao = data['orgao']
            search = data['search']
            ids = Matricula.objects.filter(orgao=orgao).values_list('id', flat=True)
            qs = User.objects.filter(matricula__in=ids).distinct()
            if(len(search) > 0):
                for term in search.split():
                    qs = qs.filter(Q(username=term) | Q(first_name__icontains=term) | Q(last_name__icontains=term))

    else:
        # Matrícula
        form = UserListForm()

    table = UserTable(qs)
    context = {'form': form, 'table':table}

    return render(request, 'registration/list_user.html', context)

