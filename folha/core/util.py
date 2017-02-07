import os
from binascii import hexlify


def create_hash():
    """This function generate 10 character long hash"""
    return hexlify(os.urandom(5))

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