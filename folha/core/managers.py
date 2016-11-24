from django.db import models

class MatriculaQuerySet(models.QuerySet):

    def matriculas_by_user(self, user):
        return self.filter(user = user).all()

    def matriculas_by_numero(self, numero, orgao):
        matricula = self.filter(numero=numero).filter(orgao=orgao).first()
        if matricula is None:
            raise ValueError('Não há cadastro da matrícula {} para o orgão {}.'.format(numero, orgao.sigla))
        return matricula

class ContraChequeQuerySet(models.QuerySet):

    def contracheques_by_matricula(self, matricula, exercicio):
        return self.filter(matricula = matricula).filter(exercicio = exercicio).all()

    def contracheques_by_matricula_mes(self, matricula, mes, exercicio):
        return self.filter(matricula = matricula).filter(mes=mes).filter(exercicio = exercicio).first()



MatriculaManager = models.Manager.from_queryset(MatriculaQuerySet)
ContraChequeManager = models.Manager.from_queryset(ContraChequeQuerySet)


