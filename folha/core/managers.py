from django.db import models

class MatriculaQuerySet(models.QuerySet):

    def matriculas_by_user(self, user):
        return self.filter(user = user).all()

    def matriculas_by_numero(self, numero, orgao):
        self.filter(numero=numero)
        self.filter(orgao=orgao)
        return self.first()

class ContraChequeQuerySet(models.QuerySet):

    def contracheques_by_matricula(self, matricula, exercicio):
        self.filter(matricula = matricula)
        self.filter(exercicio = exercicio)
        return self.all()

    def contracheques_by_matricula_mes(self, matricula, mes, exercicio):
        self.filter(matricula = matricula)
        self.filter(mes=mes)
        self.filter(exercicio = exercicio)
        return self.all()


MatriculaManager = models.Manager.from_queryset(MatriculaQuerySet)
ContraChequeManager = models.Manager.from_queryset(ContraChequeQuerySet)


