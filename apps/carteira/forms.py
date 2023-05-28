from django import forms
from apps.carteira.models import Carteira


class CarteiraBaixa(forms.ModelForm):
    categorias_gastos = {
    "Alimentação": ["Restaurantes", "Supermercado", "Delivery"],
    "Transporte": ["Gasolina", "Transporte público", "Uber/Táxi"],
    "Moradia": ["Aluguel", "Hipoteca", "Contas de serviços públicos"],
    "Lazer": ["Viagens", "Cinema", "Eventos esportivos"],
    "Saúde": ["Consultas médicas", "Medicamentos", "Seguro saúde"],
    "Educação": ["Mensalidades", "Material didático", "Cursos"],
    "Compras": ["Roupas", "Eletrônicos", "Acessórios"],
    "Contas": ["Internet", "TV a cabo", "Telefone"],
    "Dívidas": ["Cartão de crédito", "Empréstimos", "Financiamentos"],
    "Investimentos": ["Ações", "Fundos mútuos", "Poupança"]
}

    choices = ((item, item) for item, array in (categorias_gastos.items()))
    categoria = forms.ChoiceField(required=True, choices=choices)
    data = forms.DateField(required=True, widget=forms.TextInput(attrs={'type':'date'}))
    class Meta:
        model = Carteira
        exclude = ['user']
