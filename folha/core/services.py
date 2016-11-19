import PyPDF2
import pdfminer
from django.core.exceptions import ValidationError
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter, PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.pdfparser import PDFPage, PDFParser, PDFDocument
from io import StringIO

from folha.core.models import ContraCheque, Matricula


def upload_contra_cheque_file(f, orgao, formato):

    if formato == 'SAPITUR':
        contra_cheque = read_sapitur(f, orgao)

    else:
        raise ValidationError('Formato ' + formato + ' inesperado')



def read_sapitur(f, orgao):
    lines = convert_pdf_to_txt(f)

    contra_cheque = ContraCheque()

    for i, line in enumerate(lines):
        if i > 0 and str(lines[i - 1]).startswith(
                'Mat'):  # Verifica se achou a matricula baseado no prefixo Mat da linha anterior
            matricula = Matricula.objects.matriculas_by_numero(line, orgao)
            continue

        if ' / ' in line:  # Verifica se achou ano e mês baseado na regra MM / aaaa
            mesAno = line.split('/')
            contra_cheque.mes = mes_string_to_int(mesAno[0].strip())
            contra_cheque.exercicio = mesAno[1].strip()

    return contra_cheque


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