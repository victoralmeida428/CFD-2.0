from django.contrib import admin
from apps.carteira.models import Carteira
class CarteiraList(admin.ModelAdmin):
    list_display = ('id', 'user', 'despesa', 'categoria','data')
    list_display_links = ('id', 'user')
    search_fields = ('user',)

admin.site.register(Carteira, CarteiraList)
