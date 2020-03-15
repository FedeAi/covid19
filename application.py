# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import json

external_stylesheets = [dbc.themes.BOOTSTRAP]

file = 'COVID-19/dati-json/dpc-covid19-ita-andamento-nazionale.json'
link = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json'
try:
    df = pd.read_json(link)
except:
    df = pd.read_json(file)



def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


def generate_ratio(a, b, start=0):
    a = df[a].values[start:]
    b = df[b].values[start:]
    ratio = a/b
    return ratio


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

badges = dbc.Container(
    [
        dbc.Badge("LinkedIn", href="https://www.linkedin.com/in/federico-sarrocco-6240b5164/",
                  color="primary", className="mr-1"),
        dbc.Badge("Mail", href="mailto:federico.sarrocco@mail.polimi.it",
                  color="secondary", className="mr-1"),
        dbc.Badge("Instagram", href="https://www.instagram.com/fedesarrocco/",
                  color="success", className="mr-1"),
        html.Br(),
        html.Br(),
        # dbc.Alert(
        #    [
        #        "Supporta il progetto: ",
        #        html.A("PayPal", href="https://paypal.me/Sarrocco?locale.x=it_IT",
        #               className="alert-link"),
        #    ],
        #    color="warning",
        # ),

    ]
)

graphs = dbc.Container([
    dcc.Graph(
        figure=dict(
            data=[

                dict(
                    x=df['data'].values,
                    y=df['totale_ospedalizzati'].values,
                    name='Totale Ospedalizzati',
                    marker=dict(
                        color='rgb(200, 83, 10)'
                    )
                ),

                dict(
                    x=df['data'].values,
                    y=df['ricoverati_con_sintomi'].values,
                    name='Ricoverati',
                    marker=dict(
                        color='rgb(55, 83, 109)'
                    )
                ),

                dict(
                    x=df['data'].values,
                    y=df['terapia_intensiva'].values,
                    name='Terapia Intensiva',
                    marker=dict(
                        color='rgb(20, 150, 180)'
                    )
                ),
                dict(
                    x=df['data'].values,
                    y=df['totale_attualmente_positivi'].values,
                    name='Totale Attualmente Positivi',
                    marker=dict(
                        color='rgba(55, 83, 109,  0.2)'
                    )
                ),
            ],
            layout=dict(
                xaxis=dict(
                    fixedrange=True
                ),
                yaxis=dict(
                    autorange='false',
                    fixedrange=True
                ),
                title='Ospedalizzati',
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 400},
        id='ospedalizzati'
    ),

    html.Br(),
    html.Br(),
    dcc.Graph(
        figure=dict(
            data=[
                dict(
                    x=df['data'].values[3:],
                    y=generate_ratio('totale_attualmente_positivi',
                                     'dimessi_guariti', start=3),
                    name='Positivi / Guariti',
                    marker=dict(
                        color='rgb(0, 255, 0)'
                    )
                ),


            ],
            layout=dict(
                xaxis=dict(
                    fixedrange=True
                ),
                yaxis=dict(
                    autorange='false',
                    fixedrange=True
                ),
                title='Totale / Guariti',
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 400},
        id='isolati'
    ),
    html.Br(),
    dbc.Container([
        html.P('''
        Rappresentato il rapporto tra il numero totale di casi e i dimessi-guariti. Quando la curva crese significa che l'incremento percentuale di nuovi casi è maggiore dell'incremento percentuale di guariti. Un valore > 1 evidenzia che i guariti sono in numero inferiore rispetto ai malati. 
    '''),
    ]),


    html.Br(),
    html.Br(),
    dcc.Graph(
        figure=dict(
            data=[
                dict(
                    x=df['data'].values[3:],
                    y=generate_ratio('tamponi', 'totale_casi'),
                    name='Tamponi / Positivi',
                    marker=dict(
                        color='rgb(20, 20, 250)'
                    )
                ),
                dict(
                    x=df['data'].values[3:],
                    y=generate_ratio('totale_ospedalizzati',
                                     'terapia_intensiva'),
                    name='Ospedalizzati / Terapia Intensiva',
                    marker=dict(
                        color='rgba(160, 0, 130, 0.5)'
                    )
                ),
                dict(
                    x=df['data'].values[3:],
                    y=generate_ratio('totale_ospedalizzati',
                                     'isolamento_domiciliare'),
                    name='Ospedalizzati / Isolamento dom.',
                    marker=dict(
                        color='rgba(160, 220, 0, 0.5)'
                    )
                ),



            ],
            layout=dict(
                xaxis=dict(
                    fixedrange=True
                ),
                yaxis=dict(
                    autorange='false',
                    fixedrange=True
                ),
                title='Tamponi / Positivi   &   Ospedalizzati / Terapia Intensiva',
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30)
            )
        ),

        style={'height': 400},
        id='tamponi'
    ),
    html.Br(),
    html.Div(children=html.P('''
        Un andamento decrescente della curva blu sottolinea l'incremento di positivi rispetto al numero di tamponi fatti giornalmente. Quando la curva blu comincerà a crescere la percentuale di positivi rispetto ai tamponi fatti diminuisce. 
    ''')),
],
    className="mt-4",)

heading = dbc.Container([
    html.Center(html.H1(children='Covid-19 Real-Time')),

    html.Div(children=html.H3('''
        Visualizzazione grafica
    ''')),
    dbc.Row([
        dbc.Col(html.H3(["positivi: ", dbc.Badge(str(
            df.iloc[-1].totale_attualmente_positivi), color="danger", className="ml-1")])),
        dbc.Col(html.H3(["guariti: ",  dbc.Badge(
            str(df.iloc[-1].dimessi_guariti), color="success", className="ml-1")])),
        dbc.Col(html.H3(["terapia intensiva: ",  dbc.Badge(
            str(df.iloc[-1].terapia_intensiva), color="warning", className="ml-1")])),
    ]),

    # generate_table(df)
    html.Br(),
    html.Br(),
],
    className="mt-4",)

app.layout = html.Div([heading, graphs, badges])

application = app.server
if __name__ == '__main__':
    application.run(debug=True, port=8080)
