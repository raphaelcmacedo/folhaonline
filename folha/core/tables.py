import django_tables2 as tables

from folha.core.models import ContraCheque


class ContraChequeTable(tables.Table):
    class Meta:
        model = ContraCheque
        attrs = {'class': 'paleblue'}
        fields = ('mes', 'url')
