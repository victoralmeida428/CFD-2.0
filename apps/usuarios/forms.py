from django import forms
from apps.usuarios.models import Usuarios
from datetime import date
import re
from apps.usuarios.models import Usuarios


class Cadastro(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'type':'password'}))
    senha_conf = forms.CharField(widget=forms.PasswordInput(attrs={'type':'password'}))
    nascimento = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model = Usuarios
        fields = '__all__'
    ## VALIDAÇÃO DOS CAMPOS
    def clean_nome(self):
        nome = self.cleaned_data['nome']
        padrao = re.compile('\d')
        if padrao.findall(nome):
            raise forms.ValidationError('Não pode conter números no nome')
        return nome
    
    def clean_senha_conf(self):
        senha = self.cleaned_data['senha']
        senha_conf = self.cleaned_data['senha_conf']
        if senha != senha_conf:
            raise forms.ValidationError('Senhas incompatíveis')
        return senha_conf
    
    def clean_nascimento(self):
        nascimento = self.cleaned_data['nascimento']
        idade = self.__calculateAge(nascimento)
        if idade < 18:
            raise forms.ValidationError('Proíbido menores de 18 anos')
        return nascimento
    
    def __calculateAge(self, born): 
        today = date.today() 
        try:  
            birthday = born.replace(year = today.year)
        except ValueError:  
            birthday = born.replace(year = today.year, 
                    month = born.month + 1, day = 1) 
    
        if birthday > today: 
            return today.year - born.year - 1
        else: 
            return today.year - born.year 


class Login(forms.Form):
    login = forms.CharField(max_length=20, required=True)
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'type':'password'}))
  
    def clean_login(self):
        login = self.cleaned_data['login']
        user = Usuarios.objects.filter(login=login).values()
        if not user:
            raise forms.ValidationError('Usuário Inválido')
        return login
    
    def clean_senha(self):
        login = self.cleaned_data.get('login')
        senha = self.cleaned_data['senha']
        user = Usuarios.objects.filter(login=login).values()
        try:
            password = user[0]['senha']
            if senha!=password:
                raise forms.ValidationError('Senha Inválida')
        except:
            return senha
        return senha
        
