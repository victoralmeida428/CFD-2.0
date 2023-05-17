from django.shortcuts import render
from django.views.generic import FormView
from apps.carteira.forms import CarteiraBaixa
from apps.carteira.models import Carteira
from apps.usuarios.models import Usuarios
from django.urls import reverse_lazy
import datetime as dt
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
from django.contrib import messages
from dash.dependencies import Input, Output
from dash import Dash, html, dcc, callback

# Create your views here.
class FormCarteira(FormView):
    template_name = 'carteira/despesa.html'
    form_class = CarteiraBaixa
    success_url = reverse_lazy('dash')
    def form_valid(self, form):
        user = self.request.user
        hoje = dt.date.today()
        despesa = form.cleaned_data['despesa']
        categoria = form.cleaned_data['categoria']
        banco = Carteira(user=user, data=hoje, despesa=despesa, categoria=categoria)
        banco.save()

        return super().form_valid(form)

def dash(request):
    user = request.user
    carteira = Carteira.objects.filter(user=user).values()
    df = pd.DataFrame(carteira)
    app = DjangoDash('carteira', add_bootstrap_links=True)
    app.css.append_css({"external_url": "/static/styles/style.css"})
    app.layout = html.Div(
        children=[
            html.Div(className='Filtros', children=[
                                            dbc.Container(id='filters', children=[
                                                        dbc.Row([
                                                            dbc.Col(dcc.DatePickerRange(id='datarange', start_date=dt.date(2023,4,1),
                                                                                        end_date=dt.datetime.now()), md=4),
                                                            dcc.Dropdown(list(df.categoria.unique()), list(df.categoria.unique())[0],
                                                                         id='categoria', style={'width':'30vw'}, multi=True)
                                                        ])])
                                    ]),            
                        dcc.Graph(id='graficogasto')
            ])
    
    @app.callback(Output('graficogasto', 'figure'),
                  Input('categoria', 'value'))
    def gasto(categoria):
        user = request.user
        carteira = Carteira.objects.filter(user=user).values()
        df = pd.DataFrame(carteira)
        df = df.groupby('categoria').sum(numeric_only=True).reset_index()
        if isinstance(categoria, list):
            df = df.loc[df.categoria.isin(categoria)]
        else:
            df = df.loc[df.categoria==categoria]
        fig = px.bar(df, x='categoria', y='despesa', color='categoria',
                     labels={'categoria':''}, text_auto=True)
        return fig

    salario = Usuarios.objects.filter(login=user).values('salario')
    nome = Usuarios.objects.filter(login=user).values('nome')
    salario = salario[0]['salario'] - df.despesa.sum()
    salario = f'{salario:,.2f}'
    context = {
        'dash_html': app,
        'salario': salario,
        'login': nome[0]['nome']
    }

    return render(request, 'carteira/carteira.html', context)