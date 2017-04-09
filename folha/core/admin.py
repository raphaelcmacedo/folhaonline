from django.contrib import admin

# Register your models here.
from folha.core.models import Orgao, Matricula, ContraCheque, Gestor

class GestorModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'orgao']
    list_filter = ('orgao__sigla',)

class MatriculaModelAdmin(admin.ModelAdmin):
    list_display = ['numero', 'orgao', 'user']
    search_fields = ('numero', 'orgao__sigla')

class ContraChequeModelAdmin(admin.ModelAdmin):
    list_display = ['matricula', 'mes', 'exercicio']
    search_fields = ('matricula__numero', 'mes', 'exercicio')


admin.site.register(Orgao)
admin.site.register(Gestor, GestorModelAdmin)
admin.site.register(Matricula, MatriculaModelAdmin)
admin.site.register(ContraCheque, ContraChequeModelAdmin)