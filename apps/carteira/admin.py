from django.contrib import admin
from apps.carteira.models import Carteira, Conta
class CarteiraList(admin.ModelAdmin):
    list_display = ('id', 'user', 'despesa', 'categoria','data')
    list_display_links = ('id', 'user')
    search_fields = ('user',)

class ContaList(admin.ModelAdmin):
    list_display = ('id', 'user', 'conta')
    list_display_links = ('id', 'user')

admin.site.register(Carteira, CarteiraList)

admin.site.register(Conta, ContaList)

