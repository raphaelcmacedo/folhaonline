from django.core.exceptions import ValidationError

from folha.core.connectors.cambuci import read_matricula_cambuci, read_contra_cheque_cambuci
from folha.core.connectors.dirf import read_informe_rendimento
from folha.core.connectors.sapitur import read_contra_cheque_sapitur, read_matricula_sapitur
from folha.core.google import insert_file
from folha.core.models import Matricula

def upload_contra_cheque_file(f, orgao, formato, matriculas_dict):

    contra_cheques = []
    if formato == 'SAPITUR':
        contra_cheque = read_contra_cheque_sapitur(f, matriculas_dict)
        contra_cheques.append(contra_cheque)
    elif formato == 'CAMBUCI':
        contra_cheque = read_contra_cheque_cambuci(f, matriculas_dict)
        contra_cheques.append(contra_cheque)
    elif formato == 'DIRF':
        contra_cheques = read_informe_rendimento(f, orgao)
    else:
        raise ValidationError('Formato ' + formato + ' inesperado')

    for contra_cheque in contra_cheques:
        validate_contra_cheque(contra_cheque)
        insert_file(contra_cheque,f)
        contra_cheque.save()


def register_matricula(f, orgao, formato):

    if formato == 'SAPITUR':
        matricula = read_matricula_sapitur(f)
    elif formato == 'CAMBUCI':
        matricula = read_matricula_cambuci(f)
    else:
        raise ValidationError('Formato ' + formato + ' inesperado')
    matricula.orgao = orgao

    try: # Caso a matrícula já exista esse metódo não retornará erro e como nada foi added retornarmos None
        Matricula.objects.matriculas_by_numero(matricula.numero, orgao)
        return None
    except:# Matrícula não existente, salva a nova matrícula e a retorna para ser added a lista
        matricula.save()
        return matricula

    else:
        raise ValidationError('Formato ' + formato + ' inesperado')


def validate_contra_cheque(contra_cheque):
    if contra_cheque.matricula_id is None:
        raise ValueError('Não foi possível localizar a matrícula neste arquivo. Verifique se este é um formato de contracheque válido')

    if contra_cheque.mes is None:
        raise ValueError('Não foi possível localizar o mês neste arquivo. Verifique se este é um formato de contracheque válido')

    if contra_cheque.exercicio is None:
        raise ValueError('Não foi possível localizar o exercício neste arquivo. Verifique se este é um formato de contracheque válido')



