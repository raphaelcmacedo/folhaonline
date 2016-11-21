from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import resolve_url

from folha.core.managers import MatriculaManager, ContraChequeManager
from folha.core.util import _createHash


class Orgao (models.Model):
    TRAJANO_DE_MORAES = '001'

    MUNICIPIOS = (
        (TRAJANO_DE_MORAES, 'Trajano de Moraes'),

    )

    sigla = models.CharField('Sigla', max_length=20)
    nome = models.CharField('Nome', max_length=100)
    municipio = models.CharField('Município', max_length=100, choices=MUNICIPIOS)

    def __str__(self):
        return self.sigla + ' ' + self.nome

class Matricula (models.Model):
    numero = models.CharField('Número', max_length=100)
    orgao = models.ForeignKey('Orgao')
    user = models.ForeignKey(User)

    objects = MatriculaManager()

    def __str__(self):
        return self.numero + ' - ' + str(self.orgao)

    def get_absolute_url(self):
        return resolve_url('matricula_detail',self.pk)


class ContraCheque(models.Model):
    matricula = models.ForeignKey('Matricula')
    exercicio = models.IntegerField('Exercício')
    mes = models.IntegerField('Mês')
    url = models.URLField()

    objects = ContraChequeManager()

    def save(self, *args, **kwargs):
        old = ContraCheque.objects.contracheques_by_matricula_mes(self.matricula, self.mes, self.exercicio)
        if old is not None:
            old.delete()

        super(ContraCheque, self).save(*args, **kwargs)


    def mes_extenso(self):
        meses = {
            0: '-',
            1: 'Janeiro',
            2: 'Fevereiro',
            3: 'Março',
            4: 'Abril',
            5: 'Maio',
            6: 'Junho',
            7: 'Julho',
            8: 'Agosto',
            9: 'Setembro',
            10: 'Outubro',
            11: 'Novembro',
            12: 'Dezembro',
        }

        return meses[self.mes]

