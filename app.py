from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
data=pd.read_csv('pollution_us_2000_2016.csv')
data2=data[data['Date Local'].str.slice(0,4).astype(int) >= 2006]

#app = Dash(__name__)
# app.layout = dbc.Container(
#     dbc.Alert("Hello Bootstrap!", color="success"),
#     className="p-5",
# )

def statewisedist(year, gas):
    data3=data2.loc[(data2['Date Local'].str.slice(0,4).astype(int) >= year[0])
                    &(data2['Date Local'].str.slice(0,4).astype(int) <= year[1]),['State',gas[0],gas[1],gas[2]]]
    data3=data3.groupby(['State',gas[2]], as_index=False).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data3['State'],
        y=data3[gas[0]],
        name='Mean ({unit})'.format(unit=data3[gas[2]][0]),
        marker_color='#2774AE'))
    fig.add_trace(go.Bar(
    x=data3['State'],
    y=data3[gas[1]],
    name='AQI',
    marker_color='#FFD100'
    ))
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                      'paper_bgcolor': 'rgba(0, 0, 0, 0)'},
                      barmode='group', xaxis_tickangle=-45,bargap=0.15,bargroupgap=0.1,
                      title={
                          'text': "Air Quality across States",
                          'y':0.9,
                          'x':0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'},
                      legend=dict(
                          orientation="h",
                          yanchor="bottom",
                          y=1.02,
                          xanchor="right",
                          x=1
                      ),
                      xaxis_title="State",
                      yaxis_title="Measure"
                      )
    
    return fig

def temporaldist(state, gas):
    data5=data2.loc[(data2['State'] == state),['State','Date Local',gas[0],gas[1],gas[2]]]
    data5['Year']=data5['Date Local'].str.slice(0,4)
    data5.drop(['Date Local'],axis=1,inplace=True)
    data5=data5.groupby(['State','Year',gas[2]], as_index=False).mean()
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data5['Year'], y=data5[gas[1]], mode='lines',
                             name='AQI',
                             line=dict(color='#003B5C', width=2),
                             connectgaps=True
    ))

    # endpoints
    fig.add_trace(go.Scatter(
        x=data5['Year'],
        y=data5[gas[1]],
        mode='markers',
        marker=dict(color='#003B5C', size=8),
        name="",
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(x=data5['Year'], y=data5[gas[0]], mode='lines',
                             name='Mean ({unit})'.format(unit=data5[gas[2]][0]),
                             line=dict(color='#F47C30', width=4),
                             connectgaps=True
    ))

    # endpoints
    fig.add_trace(go.Scatter(
        x=data5['Year'],
        y=data5[gas[0]],
        mode='markers',
        marker=dict(color='#F47C30', size=12),
        name="",
        showlegend=False
    ))
    
    fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                      'paper_bgcolor': 'rgba(0, 0, 0, 0)'},
                      title={
                          'text': "Temporal trend",
                          'y':0.9,
                          'x':0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'},
                      legend=dict(
                          orientation="h",
                          yanchor="bottom",
                          y=1.02,
                          xanchor="right",
                          x=1
                      ),
                      xaxis_title="Year",
                      yaxis_title="Measure")
    
    return fig


navbar = dbc.Navbar(
    dbc.Container(
        [
#             html.A(
#                 # Use row and col to control vertical alignment of logo / brand
#                 dbc.Row(
#                     [
#                         dbc.Col(html.Img(src='logo_UCLA_blue_boxed.png', height="30px")),
#                         dbc.Col(dbc.NavbarBrand("Navbar", className="ms-2")),
#                     ],
#                     align="center",
#                     className="g-0",
#                 ),
#                 href="#",
#                 style={"textDecoration": "none"},
#             ),
#             dbc.Row(
#                     [
#                         dbc.Col(html.Img(src='logo_UCLA_blue_boxed.png', height="30px"),width=1),
#                         dbc.Col(html.P("Navbar", style={ 'display': 'flex',  'justify-content':'center', 'color':'#F1F1F1'}),width=10),
#                         dbc.Col(width=1)
#                     ],
#                     align="center",
#                     className="g-0",
#                 ),
            html.A(
                dbc.Row(
                    dbc.Col(dbc.NavbarBrand("Air Quality Index Dashboard", className="ms-2")),
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            )
        ],fluid=True
    ),
    color="dark",
    dark=True,
)

card1=dbc.Card([
    dbc.CardHeader("State-wise Pollution",style={'color': '#313339'}),
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col([
                    html.P("Year",style={ 'display': 'flex',  'justify-content':'center'})],width=6),
                dbc.Col([
                    html.P("Gas",style={ 'display': 'flex',  'justify-content':'center'})],width=6)]),
            dbc.Row([
                dbc.Col([
                    
                    dcc.RangeSlider(2006, 2016,
                                    id='year',
                                    marks={i: '{}'.format(i) for i in range(2006,2017)},
                                    value=[2006,2017],
                                    #dots=False,
                                    step=1,
                                    #updatemode='drag'
                                   )
                ],width=6),
                dbc.Col(dcc.Dropdown(
                    options = [{'label': x, 'value': x} for x in ['CO','NO2','O3','SO2']],
                    value='CO',
                    id='gas_select')
                        ,width=6)]),
            dbc.Row([dbc.Col(dcc.Graph(id="statedist"))]),
            dbc.Row([dbc.Col(html.P(id="test"))])
                ])
    
],className="mb-3 x-3")

card2=dbc.Card([
    dbc.CardHeader("Temporal Trend"),
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col([
                    html.P("State",style={ 'display': 'flex',  'justify-content':'center'})],width=6),
                dbc.Col([
                    html.P("Gas",style={ 'display': 'flex',  'justify-content':'center'})],width=6)]),
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(options = [{'label': x, 'value': x} for x in set(data2['State'].tolist())],
                    value='Arizona',
                    id='state_select')
                ,width=6),
                dbc.Col(dcc.Dropdown(options = [{'label': x, 'value': x} for x in ['CO','NO2','O3','SO2']],
                    value='CO',
                    id='gas_select2')
                        ,width=6)]),
            dbc.Row([dbc.Col(dcc.Graph(id="timedist"))])
                ])
    
],className="mb-3 x-3")

app.layout = html.Div([
    dbc.Row([dbc.Col(navbar)],className="mb-4"),
    dbc.Row([dbc.Col(card1)],className="mb-4 ml-3"),
    dbc.Row([dbc.Col(card2)],className="mb-4 ml-3")
])


@callback(
    Output('statedist', 'figure'),
    [Input('year', 'value'),
     Input('gas_select', 'value')]
)
def update_statew(year,gas):
    gas_units = ['{k} Mean'.format(k=gas),'{k} AQI'.format(k=gas),'{k} Units'.format(k=gas)]
    fig=statewisedist(year,gas_units)
    return fig

@callback(
    Output('timedist', 'figure'),
    [Input('state_select', 'value'),
     Input('gas_select2', 'value')]
)
def update_timew(state,gas):
    gas_units = ['{k} Mean'.format(k=gas),'{k} AQI'.format(k=gas),'{k} Units'.format(k=gas)]
    fig=temporaldist(state,gas_units)
    return fig

if __name__ == '__main__':
    app.run(debug=True)
