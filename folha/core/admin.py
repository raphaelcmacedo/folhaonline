from django.contrib import admin

# Register your models here.
from folha.core.models import Orgao, Matricula, ContraCheque, Gestor


class MatriculaModelAdmin(admin.ModelAdmin):
    list_display = ['numero', 'orgao', 'user']

class ContraChequeModelAdmin(admin.ModelAdmin):
        list_display = ['matricula', 'mes', 'exercicio']


class GestorModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'orgao']

admin.site.register(Orgao)
admin.site.register(Matricula, MatriculaModelAdmin)
admin.site.register(ContraCheque, ContraChequeModelAdmin)
admin.site.register(Gestor, GestorModelAdmin)