import re

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from folha.core.connectors.pdf import convert_pdf_to_txt
from folha.core.util import mes_string_to_int

REGEX_MATRICULA_CAMBUCI = r'^\d+\s+\w+\s+\w+'

def read_contra_cheque_cambuci(f, matriculas_dict):
    lines = convert_pdf_to_txt(f)

    from folha.core.models import ContraCheque
    contra_cheque = ContraCheque()

    for i, line in enumerate(lines):
        if re.search(REGEX_MATRICULA_CAMBUCI, line):
            key = line.split(' ')[0]
            try:
                contra_cheque.matricula = matriculas_dict[key]
            except:
                raise ValueError('Matrícula {} não cadastrada'.format(key))

            continue

        if 'Referencia:' in line:  # Verifica se achou ano e mês baseado na regra MM / aaaa
            line = line.replace('Referencia:', '').replace('.', '').strip()
            mesAno = line.split('/')
            contra_cheque.mes = mes_string_to_int(mesAno[0].strip())
            contra_cheque.exercicio = mesAno[1].strip()

    return contra_cheque


def read_matricula_cambuci(f):
    lines = convert_pdf_to_txt(f)

    from folha.core.models import Matricula
    matricula = Matricula()

    # Busca o número da matrícula
    for i, line in enumerate(lines):

        if re.search(REGEX_MATRICULA_CAMBUCI, line):
            parts = line.split(' ')
            matricula.numero = ''
            nome = ''
            sobrenome = ''
            for part in parts:
                if len(part) > 0:#part possui valor
                    if len(matricula.numero) <= 0:
                        matricula.numero = part
                    elif len(nome) <= 0:
                        nome = part.title()
                    else:
                        sobrenome = sobrenome + ' ' + part.title()
            sobrenome = sobrenome.strip()[:30]


    # O login do usuário no caso desse modelo é a própria matrícula, já que não há os dados de CPF nesse sistema
    try:
        user = User.objects.get(username=matricula.numero)
    except ObjectDoesNotExist:
        user = User()
        user.username = matricula.numero
        user.password = make_password(matricula.numero)
        user.first_name = nome
        user.last_name = sobrenome
        user.save()
    matricula.user = user

    return matricula
