from django.db import models
from django.contrib.auth.models import User
class Carteira(models.Model):
    fixa_variavel = (
        ('fixa', 'Fixa'),
        ('variavel', 'Variável')
    )
    renda = models.CharField(choices=fixa_variavel, blank=False, max_length=20)
    despesa = models.FloatField(max_length=20)
    categoria = models.CharField(max_length=20)
    data = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

