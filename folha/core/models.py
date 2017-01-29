from django.contrib.auth.models import User, Group
from django.db import models
from django.shortcuts import resolve_url
from django.db.models import signals

from folha.core.managers import MatriculaManager, ContraChequeManager


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
            #delete_file(old)

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

#Customize user
def is_admin(self):
    return self.groups.filter(name='admin').exists()

def is_change_password(self):
    return self.groups.filter(name='change_password').exists()

def add_change_password(self):
    group = Group.objects.get(name='change_password')
    group.user_set.add(self)

def remove_change_password(self):
    group = Group.objects.get(name='change_password')
    group.user_set.remove(self)

User.add_to_class("is_admin",is_admin)
User.add_to_class("is_change_password",is_change_password)
User.add_to_class("add_change_password",add_change_password)
User.add_to_class("remove_change_password",remove_change_password)

def create_user_profile_signal(sender, instance, created, **kwargs):
    if created:
        instance.add_change_password();

def password_change_signal(sender, instance, **kwargs):
    try:
        user = User.objects.get(username=instance.username)
        if not user.password == instance.password:
          instance.remove_change_password();
    except User.DoesNotExist:
        pass

signals.pre_save.connect(password_change_signal, sender=User, dispatch_uid='accounts.models')
signals.post_save.connect(create_user_profile_signal, sender=User, dispatch_uid='accounts.models')