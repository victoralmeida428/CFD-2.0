from django.shortcuts import render
from django.views.generic import FormView
from apps.carteira.forms import CarteiraBaixa
from apps.carteira.models import Carteira
from apps.usuarios.models import Usuarios
from django.urls import reverse_lazy
import datetime as dt
import pandas as pd
import plotly.express as px
import dash_table as dtable
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
        data = form.cleaned_data['data']
        despesa = form.cleaned_data['despesa']
        categoria = form.cleaned_data['categoria']
        banco = Carteira(user=user, data=data, despesa=despesa, categoria=categoria)
        banco.save()

        return super().form_valid(form)

def dash(request):
    user = request.user
    carteira = Carteira.objects.filter(user=user).values()
    df = pd.DataFrame(carteira)
    app = DjangoDash('carteira', add_bootstrap_links=True)
    app.css.append_css({"external_url": "/static/styles/style.css"})
    try:
        app.layout = html.Div(
            children=[
                html.Div(className='Filtros', children=[
                                                dbc.Container(id='filters', children=[
                                                            dbc.Row([
                                                                dbc.Col(dcc.DatePickerRange(id='datarange', start_date=dt.date(2023,4,1),
                                                                                            end_date=dt.datetime.now()), md=4),
                                                                dcc.Dropdown(list(df.categoria.unique()), list(df.categoria.unique()),
                                                                            id='categoria', style={'width':'30vw'}, multi=True)
                                                            ])])
                                        ]),            
                            dbc.Container(id='graficos', children=[
                                dbc.Row([
                                    dbc.Col(dcc.Graph(id='maioresgastos')),
                                    dbc.Col([dtable.DataTable(id='extrato',
                                                            data=df[['data', 'categoria', 'despesa']].to_dict('records'),
                                                            columns=[{'id':c, 'name':c} for c in df[['data', 'categoria', 'despesa']].columns],
                                                            style_as_list_view=True,
                                                            row_deletable=True,
                                                            page_size=10,
                                                            filter_action='native',
                                                            filter_options={'placeholder_text':'Filtrar coluna'},
                                                            sort_action='native',                                                
                                                            sort_mode='multi',
                                                            style_cell={'textAlign': 'center'}
                                                            ),
                                            dbc.Alert(id='Alerta')])
                                ]),
                                dbc.Row([
                                    dbc.Col(dcc.Graph(id='Linha'))
                                ])
                            ])
                ])
        
        @app.callback(Output('maioresgastos', 'figure'),
                    [Input('categoria', 'value'),
                    Input('extrato', 'derived_virtual_data')])
        def gasto(categoria, row):
            user = request.user
            carteira = Carteira.objects.filter(user=user).values()
            df = pd.DataFrame(carteira)
            df = df if row is None else pd.DataFrame(row)
            now = dt.datetime.now()
            df.data = pd.to_datetime(df.data)
            print(df.info())
            df = df.groupby('categoria').sum(numeric_only=True).reset_index()
            if isinstance(categoria, list):
                df = df.loc[df.categoria.isin(categoria)]
            else:
                df = df.loc[df.categoria==categoria]
            fig = px.bar(df.sort_values('despesa', ascending=False), x='categoria', y='despesa', color='categoria',
                        labels={'categoria':''}, text_auto=True, title='<b>Gastos por categorias</b>')
            fig.update_layout(title_x=0.5)
            return fig
        
        @app.callback(Output('Alerta', 'children'),
                    [Input('extrato', 'active_cell'),
                    Input('extrato', 'derived_virtual_data')])
        def extrato(active_cell, row):  
            df = df if row is None else pd.DataFrame(row)           
            return str(df.loc[active_cell['row'], active_cell['column_id']]) if active_cell else "Click the table"
    except:
        app.layout = html.Div()
        
    
    salario = Usuarios.objects.filter(login=user).values('salario')
    nome = Usuarios.objects.filter(login=user).values('nome')
    try:
        salario = salario[0]['salario'] - df.despesa.sum()
    except:
        salario = salario[0]['salario']
    salario = f'{salario:,.2f}'
    
    context = {
        'dash_html': app,
        'salario': salario,
        'login': nome[0]['nome'],
        'validacao': len(df)>0
    }

    return render(request, 'carteira/carteira.html', context)