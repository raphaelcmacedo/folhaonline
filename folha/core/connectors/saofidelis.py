import re

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils._os import upath

from folha.core.connectors.pdf import convert_pdf_to_txt
from folha.core.util import mes_string_to_int

REGEX_MES_ANO_SAOFIDELIS = r'de \d{4}$'
REGEX_CPF = r'(^[0-9]{3}[\.][0-9]{3}[\.][0-9]{3}[-][0-9]{2})'

def read_contra_cheque_saofidelis(f, matriculas_dict):
    lines = convert_pdf_to_txt(f)

    from folha.core.models import ContraCheque
    contra_cheque = ContraCheque()

    #Matricula
    nunero_matricula = find_matricula_sao_fidelis(lines)
    try:
        contra_cheque.matricula = matriculas_dict[nunero_matricula]
    except:
        raise ValueError('Matrícula {} não cadastrada'.format(nunero_matricula))

    for i, line in enumerate(lines):
        if re.search(REGEX_MES_ANO_SAOFIDELIS, line):  # Verifica se achou ano e mês baseado na regra MMMM de aaaa
            mesAno = line.split('de')
            contra_cheque.mes = mes_string_to_int(mesAno[0].strip())
            contra_cheque.exercicio = mesAno[1].strip()
            break

    return contra_cheque

def clean_decimo_terceiro(line):
    line = line.replace('13º Salário (1º Parc.) - ', '').replace('.', '').strip()
    line = line.replace('13º Salário (2º Parc) - ', '').replace('.', '').strip()
    line = line.replace('13º Salario - Parcela Final - ', '').replace('.', '').strip()

    return line

def read_matricula_saofidelis(f):
    lines = convert_pdf_to_txt(f)

    from folha.core.models import Matricula
    matricula = Matricula()

    nome_completo = find_field_saofidelis(lines, 'NOME DO FUNCIONÁRIO')
    nome_parts = nome_completo.split(' ')

    up_to_last_30_slice = slice(-30, None)
    nome = nome_parts[0][up_to_last_30_slice]
    sobrenome = ' '.join(nome_parts[1:])[up_to_last_30_slice]
    nunero_matricula = find_matricula_sao_fidelis(lines)
    cpf = clean_cpf(find_regex_saofidelis(lines, REGEX_CPF))
    matricula.numero = nunero_matricula

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

def find_matricula_sao_fidelis(lines):
    result = lines[14]
    if result == "PIS":
        result = lines[10]

    return result


def find_field_saofidelis(lines, field):
    labelFound = False
    for line in lines:
        if(line == field):
            labelFound = True
        elif labelFound and line:
            return line

def find_regex_saofidelis(lines, regex):
    for line in lines:
        search = re.search(regex, line)
        if search:
            return search.group(0)


def clean_cpf(cpf):
    if cpf:
        return cpf.replace('.', '').replace('-', '')