import re
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFParser, PDFDocument

from folha.core.google import insert_file
from folha.core.models import ContraCheque, Matricula

REGEX_MATRICULA_SAPITUR = r'^\d+\s+\w+\s+\w+'


def upload_contra_cheque_file(f, orgao, formato):

    if formato == 'SAPITUR':
        contra_cheque = read_contra_cheque_sapitur(f, orgao)
        validate_contra_cheque(contra_cheque)
        file = insert_file(contra_cheque,f)
        contra_cheque.save()

    else:
        raise ValidationError('Formato ' + formato + ' inesperado')

def register_matricula(f, orgao, formato):

    if formato == 'SAPITUR':
        matricula = read_matricula_sapitur(f)
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
        raise ValueError('Não foi possível localizar a matrícula neste arquivo. Verifique se este é um formato de contra cheque válido')

    if contra_cheque.mes is None:
        raise ValueError('Não foi possível localizar o mês neste arquivo. Verifique se este é um formato de contra cheque válido')

    if contra_cheque.exercicio is None:
        raise ValueError('Não foi possível localizar o exercício neste arquivo. Verifique se este é um formato de contra cheque válido')


def read_contra_cheque_sapitur(f, orgao):
    lines = convert_pdf_to_txt(f)

    contra_cheque = ContraCheque()

    for i, line in enumerate(lines):
        if re.search(REGEX_MATRICULA_SAPITUR, line):
            parts = line.split(' ')
            contra_cheque.matricula = Matricula.objects.matriculas_by_numero(parts[0], orgao)

            continue

        if ' / ' in line:  # Verifica se achou ano e mês baseado na regra MM / aaaa
            mesAno = line.split('/')
            contra_cheque.mes = mes_string_to_int(mesAno[0].strip())
            contra_cheque.exercicio = mesAno[1].strip()

    return contra_cheque

def read_matricula_sapitur(f):
    lines = convert_pdf_to_txt(f)

    matricula = Matricula()

    # Busca o número da matrícula

    for i, line in enumerate(lines):

        if re.search(REGEX_MATRICULA_SAPITUR, line):
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
            sobrenome = sobrenome.strip()


    # Busca o cpf pelo nome do arquivo
    filename = str(f)
    index = filename.index('-')
    cpf = filename[:index].strip()

    # Verifica se esse cpf já possui um usuário caso contrário cadastra
    try:
        user = User.objects.get(username=cpf)
    except ObjectDoesNotExist:
        user = User()
        user.username = cpf
        user.password = cpf
        user.first_name = nome
        user.last_name = sobrenome
        user.save()
    matricula.user = user


    return matricula


def convert_pdf_to_txt(f):
    parser = PDFParser(f)
    doc = PDFDocument()
    parser.set_document(doc)
    doc.set_parser(parser)
    doc.initialize('')
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.

    lines = []

    for page in doc.get_pages():
        interpreter.process_page(page)
        layout = device.get_result()
        for lt_obj in layout:
            if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
                blocks = lt_obj.get_text().split('\n')
                for block in blocks:
                    lines.append(block)

    return lines

def mes_string_to_int(mes):
    meses = {
        '-': 0 ,
        'Janeiro': 1,
        'Fevereiro': 2,
        'Março': 3,
        'Abril': 4,
        'Maio': 5,
        'Junho': 6,
        'Julho': 7,
        'Agosto': 8,
        'Setembro': 9,
        'Outubro': 10,
        'Novembro': 11,
        'Dezembro': 12,
    }

    return meses[mes]