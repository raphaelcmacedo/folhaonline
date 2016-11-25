import django_tables2 as tables
from django_tables2.utils import A
from django.contrib.auth.models import User


class UserTable(tables.Table):
    edit = tables.LinkColumn('edit_user', args=[A('id')], orderable=False, text='Edit')

    class Meta:
        model = User
        fields = ('username', 'email', 'firstname', 'lastname')
        attrs = {"class": "paleblue"}

