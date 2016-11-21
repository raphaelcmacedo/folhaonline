from django.contrib import admin

# Register your models here.
from folha.core.models import Orgao, Matricula, ContraCheque

class MatriculaModelAdmin(admin.ModelAdmin):
    list_display = ['numero', 'orgao', 'user']

class ContraChequeModelAdmin(admin.ModelAdmin):
        list_display = ['matricula', 'mes', 'exercicio']

admin.site.register(Orgao)
admin.site.register(Matricula, MatriculaModelAdmin)
admin.site.register(ContraCheque, ContraChequeModelAdmin)