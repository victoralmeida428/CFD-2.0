from django.contrib import admin
from apps.usuarios.models import Usuarios


class UsuarioList(admin.ModelAdmin):
    list_display = ( 'nome', 'login','email', 'nascimento')
    list_display_links = ( 'nome', 'login')
    search_fields = ('nome', 'email', 'login')
    list_max_show_all = 10

admin.site.register(Usuarios, UsuarioList)

