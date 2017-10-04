from django.db import models


class MatriculaQuerySet(models.QuerySet):

    def matriculas_by_user(self, user):
        return self.filter(user = user).all()

    def matriculas_by_cpf(self, cpf):
        return self.filter(user__username = cpf).all()

    def matriculas_by_orgao(self, orgao):
        return self.filter(orgao=orgao).all()

    def matriculas_by_numero(self, numero, orgao):
        matricula = self.filter(numero=numero).filter(orgao=orgao).first()
        if matricula is None:
            raise ValueError('Não há cadastro da matrícula {} para o orgão {}.'.format(numero, orgao.sigla))
        return matricula

    def matriculas_dict_by_orgao(self,orgao):
        matriculas = self.filter(orgao=orgao)
        matriculas_dict = {}
        for matricula in matriculas:
            matriculas_dict[matricula.numero] = matricula

        return matriculas_dict

class ContraChequeQuerySet(models.QuerySet):

    def contracheques_by_matricula(self, matricula, exercicio):
        return self.filter(matricula = matricula).filter(exercicio = exercicio).all().order_by('exercicio', 'mes')

    def contracheques_by_matricula_mes(self, matricula, mes, exercicio):
        return self.filter(matricula = matricula).filter(mes=mes).filter(exercicio = exercicio).first()

class GestorQuerySet(models.QuerySet):

    def gestor_by_user(self, user):
        return self.filter(user = user).all()

    def gestor_can_change_password(self, user):
        return self.filter(user=user).filter(alterarSenhaUsuarios=True).all().count() > 0

MatriculaManager = models.Manager.from_queryset(MatriculaQuerySet)
ContraChequeManager = models.Manager.from_queryset(ContraChequeQuerySet)
GestorManager = models.Manager.from_queryset(GestorQuerySet)


