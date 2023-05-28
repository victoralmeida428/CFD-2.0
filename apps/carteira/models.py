from django.db import models
from django.contrib.auth.models import User

class Carteira(models.Model):
    despesa = models.FloatField(max_length=20)
    categoria = models.CharField(max_length=20)
    data = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Conta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conta = models.FloatField(max_length=20)
    


