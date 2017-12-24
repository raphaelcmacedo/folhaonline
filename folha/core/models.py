from django.contrib.auth.models import User, Group
from django.db import models
from django.shortcuts import resolve_url
from django.db.models import signals

from folha.core.managers import MatriculaManager, ContraChequeManager, GestorManager


class Orgao (models.Model):
    BOM_JARDIM = 'BOM_JARDIM'
    CAMBUCI = 'CAMBUCI'
    TRAJANO_DE_MORAES = 'TRAJANO_DE_MORAES'


    MUNICIPIOS = (
        (BOM_JARDIM, 'Bom Jardim'),
        (CAMBUCI, 'Cambuci'),
        (TRAJANO_DE_MORAES, 'Trajano de Moraes'),

    )

    sigla = models.CharField('Sigla', max_length=20)
    nome = models.CharField('Nome', max_length=100)
    municipio = models.CharField('Município', max_length=100, choices=MUNICIPIOS)

    class Meta:
        verbose_name = 'orgão'
        verbose_name_plural = 'orgãos'
        ordering = ('sigla',)


    def __str__(self):
        return self.sigla + ' ' + self.nome

class Gestor (models.Model):
    orgao = models.ForeignKey('Orgao')
    user = models.ForeignKey(User)
    alterarSenhaUsuarios = models.BooleanField('Alterar Senha de Outros Usuários', default=False)

    objects = GestorManager()

    class Meta:
        verbose_name = 'gestor'
        verbose_name_plural = 'gestores'


    def __str__(self):
        return str(self.orgao) + ' - ' + self.user.first_name + ' - ' + self.user.last_name



class Matricula (models.Model):
    numero = models.CharField('Número', max_length=100)
    orgao = models.ForeignKey('Orgao')
    user = models.ForeignKey(User)

    objects = MatriculaManager()

    class Meta:
        verbose_name = 'matrícula'
        verbose_name_plural = 'matrículas'
        ordering = ('numero',)


    def __str__(self):
        return '{} {} - {} ({})'.format(self.user.first_name, self.user.last_name, self.numero, self.orgao.sigla )

    def get_absolute_url(self):
        return resolve_url('matricula_detail',self.pk)


class ContraCheque(models.Model):
    matricula = models.ForeignKey('Matricula')
    exercicio = models.IntegerField('Exercício')
    mes = models.IntegerField('Mês')
    url = models.URLField()
    decimoTerceiro = models.NullBooleanField('Décimo Terceiro')

    objects = ContraChequeManager()

    class Meta:
        verbose_name = 'contra cheque'
        verbose_name_plural = 'contra cheques'


    def save(self, *args, **kwargs):
        old = ContraCheque.objects.contracheques_by_matricula_mes(self.matricula, self.mes, self.exercicio)
        if old is not None:
            old.delete()
            #delete_file(old)

        super(ContraCheque, self).save(*args, **kwargs)


    def mes_extenso(self):
        meses = {
            0: 'Informe de Rendimentos',
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

        result = meses[self.mes]

        if self.decimoTerceiro:
            result = result + ' - parcela de décimo terceiro'

        return result

#Customize user
def is_admin(self):
    #return self.groups.filter(name='admin').exists()
    return Gestor.objects.gestor_by_user(self)

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