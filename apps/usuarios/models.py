from django.db import models

class Usuarios(models.Model):
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('N', 'Neutro'),
        ('S', 'Prefiro não responder')
    )
    nome = models.CharField(max_length=50, blank=False, null=False)
    login = models.CharField(max_length=10, blank=False, null=False, unique=True)
    senha = models.CharField(max_length=15, blank=False, null=False, )
    senha_conf = models.CharField(max_length=15, blank=False, default='0000')
    email = models.EmailField(blank=False, null=False, unique=True)
    sexo = models.CharField(choices=SEXO_CHOICES, max_length=20)
    nascimento = models.DateField(blank=False, null=False)
    salario = models.FloatField()
    
    