import re

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils._os import upath

from folha.core.connectors.pdf import convert_pdf_to_txt
from folha.core.util import mes_string_to_int

REGEX_MATRICULA_CAMBUCI = r'^\d+\s+\w+\s+\w+'

def read_contra_cheque_cambuci(f, matriculas_dict):
    lines = convert_pdf_to_txt(f)

    from folha.core.models import ContraCheque
    contra_cheque = ContraCheque()

    #Matricula
    nunero_matricula = find_field_cambuci(lines, 'Matricula')
    try:
        contra_cheque.matricula = matriculas_dict[nunero_matricula]
    except:
        raise ValueError('Matrícula {} não cadastrada'.format(nunero_matricula))

    for i, line in enumerate(lines):
        if 'Folha Normal - ' in line:  # Verifica se achou ano e mês baseado na regra MM / aaaa
            line = line.replace('Folha Normal - ', '').replace('.', '').strip()
            mesAno = line.split('/')
            contra_cheque.mes = mes_string_to_int(mesAno[0].strip())
            contra_cheque.exercicio = mesAno[1].strip()
        elif '13º Salário' in line or '13º Salario' in line:  # Verifica se achou ano e mês baseado na regra MM / aaaa em caso de 13²º
            contra_cheque.decimoTerceiro = True
            line = clean_decimo_terceiro(line)
            mesAno = line.split('/')
            if len(mesAno) >= 2:
                contra_cheque.mes = mes_string_to_int(mesAno[0].strip())
                contra_cheque.exercicio = mesAno[1].strip()

    return contra_cheque

def clean_decimo_terceiro(line):
    line = line.replace('13º Salário (1º Parc.) - ', '').replace('.', '').strip()
    line = line.replace('13º Salário (2º Parc) - ', '').replace('.', '').strip()
    line = line.replace('13º Salario - Parcela Final - ', '').replace('.', '').strip()

    return line

def read_matricula_cambuci(f):
    lines = convert_pdf_to_txt(f)

    from folha.core.models import Matricula
    matricula = Matricula()

    nome_completo = find_field_cambuci(lines, 'Nome do Funcionário')
    nome_parts = nome_completo.split(' ')

    up_to_last_30_slice = slice(-30, None)
    nome = nome_parts[0][up_to_last_30_slice]
    sobrenome = ' '.join(nome_parts[1:])[up_to_last_30_slice]
    nunero_matricula = find_field_cambuci(lines, 'Matricula')
    matricula.numero = nunero_matricula

    try:
        filename = f['name']
    except:
        filename = str(f)
    index = filename.index('_')
    cpf = filename[:index].strip()

    # Verifica se esse cpf já possui um usuário caso contrário cadastra
    try:
        user = User.objects.get(username=cpf)
    except ObjectDoesNotExist:
        user = User()
        user.username = cpf
        user.password = make_password(matricula.numero)
        user.first_name = nome
        user.last_name = sobrenome
        user.save()
    matricula.user = user

    return matricula

def find_field_cambuci(lines, field):
    labelFound = False
    for line in lines:
        if(line == field):
            labelFound = True
        elif labelFound and line:
            return line



