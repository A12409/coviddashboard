from map import *
from CovidChart import *
from VaccineChart import *
from Symptoms import *
from htmlData import *
import dash
import dash_core_components as dcc
import dash_html_components as html


def get_covid_update():
    myhtml = getdata("https://www.mohfw.gov.in/")
    soup = BeautifulSoup(myhtml, 'html.parser')
    vac = soup.find("div", class_="fullbol").find_all("span")
    act = soup.find("li", class_="bg-blue").find_all("strong")[0:2]
    dis = soup.find("li", class_="bg-green").find_all("strong")[0:2]
    death = soup.find("li", class_="bg-red").find_all("strong")[0:2]
    dataList = act + dis + death
    all_data = []
    for i in range(0, len(dataList), 2):
        all_data.append((dataList[i].get_text().split("\xa0")[0].replace(" ", ""),
                         dataList[i + 1].get_text().split('\xa0\xa0\xa0\xa0\xa0')))
    vacdata = vac[1].get_text() + " " + vac[2].get_text().replace(" ", "")
    all_data.append((vac[0].get_text().split(":")[0].replace(" ", ""), vacdata.replace(",", "").split()))
    return all_data


datalist = get_covid_update()

df = covidframe[['State/UT', 'Total Cases', 'Total Deaths', 'Total Recovered', 'Active Cases', '1st Dose', '2nd Dose',
                 'Total vaccine']]

external_stylesheets = ['https://codepen.io/anon/pen/mardKv.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

theme = {
    'dark': True,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E',
}

app.layout = html.Div([
    html.Div(style={
        'backgroundColor': '#111111'
    }, children=[
        html.H1(
            children='Coronavirus [Covid-19] Interactive Outbreak Tracker',
            style={
                'textAlign': 'center',
                'color': '#7FDBFF'
            }
        ),

        html.Div(children='Dashboard : Covid-19 Outbreak.(Update once a day)based on Consolidated last day total',
                 style={
                     'textAlign': 'center',
                     'color': '#7FDBFF'
                 }),

        html.Div(children='Best Viewed on Desktop : Refresh browser for latest Update', style={
            'textAlign': 'center',
            'color': '#7FDBFF'
        }),
    ]),
    html.Div([

        html.Div([
            dcc.Dropdown(style={
                'textAlign': 'center',
                'color': '#111111',
                'backgroundColor': '#7FDBFF'
            },
                id='column',
                options=[{'label': i, 'value': i} for i in colour_dict.keys()],
                value='Active Cases'
            )
        ], style={'width': '20%', 'backgroundColor': '#111111', 'color': '#7FDBFF'}),

        html.Div([
            dcc.Graph(
                id='map'
            )], style={'width': '100%', 'display': 'blank', 'color': '#7FDBFF', 'backgroundColor': '#111111'}),
    ]),

    html.Div([
        html.Div([
            html.H5(children=datalist[0][0],
                    style={
                        'textAlign': 'center',
                        'color': '#ff781f'}
                    ),

            html.P(datalist[0][1][0],
                   style={
                       'textAlign': 'center',
                       'color': '#ff781f',
                       'fontSize': 30}
                   ),

            html.P('new:  ' + datalist[0][1][1],
                   style={
                       'textAlign': 'center',
                       'color': '#ff781f',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], style={'width': '25%', 'float': 'left', 'display': 'inline-block', 'backgroundColor': '#111111',
                              'color': '#7FDBFF'}),
        html.Div([
            html.H5(children=datalist[1][0],
                    style={
                        'textAlign': 'center',
                        'color': '#007500'}
                    ),

            html.P(datalist[1][1][0],
                   style={
                       'textAlign': 'center',
                       'color': '#007500',
                       'fontSize': 30}
                   ),

            html.P('new:  ' + datalist[1][1][1],
                   style={
                       'textAlign': 'center',
                       'color': '#007500',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], style={'width': '25%', 'float': 'left', 'display': 'inline-block', 'backgroundColor': '#111111',
                              'color': '#7FDBFF'}),
        html.Div([
            html.H5(children=datalist[2][0],
                    style={
                        'textAlign': 'center',
                        'color': '#dd1e35'}
                    ),

            html.P(datalist[2][1][0],
                   style={
                       'textAlign': 'center',
                       'color': '#dd1e35',
                       'fontSize': 30}
                   ),

            html.P('new:  ' + datalist[2][1][1],
                   style={
                       'textAlign': 'center',
                       'color': '#dd1e35',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], style={'width': '25%', 'float': 'left', 'display': 'inline-block', 'backgroundColor': '#111111',
                              'color': '#7FDBFF'}),
        html.Div([
            html.H5(children=datalist[3][0],
                    style={
                        'textAlign': 'center',
                        'color': '#FFF338'}
                    ),

            html.P(datalist[3][1][0],
                   style={
                       'textAlign': 'center',
                       'color': '#FFF338',
                       'fontSize': 30}
                   ),

            html.P('new:  ' + datalist[3][1][1],
                   style={
                       'textAlign': 'center',
                       'color': '#FFF338',
                       'fontSize': 15,
                       'margin-top': '-18px'}
                   )], style={'width': '25%', 'float': 'left', 'display': 'inline-block', 'backgroundColor': '#111111',
                              'color': '#7FDBFF'}),
    ]),

    html.Div(children=' ', style={
        'textAlign': 'center',
        'color': '#7FDBFF',
        'fontSize': 20
    }),

    html.Div(children='Current Covid-19 Situation in INDIA [State] ', style={
        'textAlign': 'center',
        'color': '#7FDBFF',
        'fontSize': 20
    }),

    html.Div(children='Total [Cumulutive] Number of Cases of Covid-19 in INDIA.', style={
        'textAlign': 'center',
        'color': '#7FDBFF'
    }),
    html.Div(children='Time Series Analysis Graph',
             style={
                 'textAlign': 'center',
                 'color': '#7FDBFF'
             }),
    html.Div([
        dcc.Dropdown(style={
            'textAlign': 'center',
            'color': '#111111',
            'backgroundColor': '#7FDBFF'
        },
            id='state',
            options=[{'label': i, 'value': i} for i in firstdose],
            value='India'

        )
    ], style={'width': '20%', 'backgroundColor': '#111111', 'color': '#7FDBFF'}),

    html.Div([
        dcc.Graph(id="covid"),
    ]),
    html.Div(children='Covid-19 Vaccination Progress in INDIA', style={
        'textAlign': 'center',
        'color': '#7FDBFF',
        'fontSize': 20
    }),

    html.Div(children='Monthly Data of Number of Covid Vaccinations',
             style={
                 'textAlign': 'center',
                 'color': '#7FDBFF'
             }),
    html.Div(children='[First Dose, Secound Dose]', style={
        'textAlign': 'center',
        'color': '#7FDBFF'
    }),
    html.Div([
        dcc.Graph(
            id='vaccine')
    ]),

    html.Div(children='Symptoms of Coronavirus Disease [Covid-19]', style={
        'textAlign': 'center',
        'color': '#7FDBFF',
        'fontSize': 20
    }),

    html.Div([
        dcc.Graph(
            id='symptom',
            figure=fig
        )
    ]),

    html.Div(children='Covid-19 Cases or Vaccination Summary in INDIA', style={
        'textAlign': 'center',
        'color': '#7FDBFF'
    }),
    html.Div(children='Data Table', style={
        'textAlign': 'center',
        'color': '#7FDBFF'
    }),

    dash_table.DataTable(
        style_cell={
            'whiteSpace': 'normal',
            'height': 'auto',
            'color': '#7FDBFF',
            'backgroundColor': 'rgb(50, 50, 50)',
        },
        style_header={
            'backgroundColor': '#111111',
            'fontWeight': 'bold'
        },
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )
], style={'backgroundColor': '#111111', 'color': '#7FDBFF'})


@app.callback(
    dash.dependencies.Output('map', 'figure'),
    [dash.dependencies.Input('column', 'value')])
def update_graph(column):
    fig = px.choropleth_mapbox(covidframe,
                               locations='id',
                               geojson=india_states,
                               color=column,
                               hover_name='State/UT',
                               hover_data=[column],
                               mapbox_style='carto-darkmatter',
                               center={'lat': 24, 'lon': 78},
                               color_continuous_scale=colour_dict[column],
                               opacity=opacity_dict[column],
                               zoom=3)

    fig.update_layout(paper_bgcolor='#111111')

    return fig


@app.callback(
    dash.dependencies.Output('covid', 'figure'),
    [dash.dependencies.Input('state', 'value')])
def update_covid_graph(state):
    temp = date_wise_data.copy()
    if state == 'India':
        confirme = temp['Confirmed']
        death = temp['Deaths']
        cure = temp['Cured']
        act = temp['Active']
    else:
        confirme = confirmed[state]
        death = deaths[state]
        cure = cured[state]
        act = active[state]

    labels = ['Confirmed', 'Deaths', 'Cured', 'Active']
    colors = ['rgb(0,128,0)', 'rgb(255,0,0)', 'rgb(49,130,189)', 'rgb(255, 127, 80)']

    line_size = [3, 3, 3, 3]

    covid_fig = go.Figure()

    covid_fig.add_trace(go.Scatter(x=temp['Date'],
                                   y=confirme, mode='lines',
                                   name=labels[0],
                                   line=dict(color=colors[0], width=line_size[0]),
                                   connectgaps=True,
                                   ))
    covid_fig.add_trace(go.Scatter(x=temp['Date'],
                                   y=death, mode='lines',
                                   name=labels[1],
                                   line=dict(color=colors[1], width=line_size[1]),
                                   connectgaps=True,
                                   ))

    covid_fig.add_trace(go.Scatter(x=temp['Date'],
                                   y=cure, mode='lines',
                                   name=labels[2],
                                   line=dict(color=colors[2], width=line_size[2]),
                                   connectgaps=True,
                                   ))

    covid_fig.add_trace(go.Scatter(x=temp['Date'],
                                   y=act, mode='lines',
                                   name=labels[3],
                                   line=dict(color=colors[3], width=line_size[3]),
                                   connectgaps=True,
                                   ))

    annotations = []

    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1,
                            xanchor='center', yanchor='top',
                            text='Date',
                            font=dict(family='Arial',
                                      size=12,
                                      color='rgb(150,150,150)'),
                            showarrow=False))

    covid_fig.update_layout(annotations=annotations, plot_bgcolor='#111111', yaxis_title='Cumulative cases',
                            font=dict(color='#7FDBFF'))
    covid_fig.update_layout(title_text='COVID-19 Cases in ' + state,
                            plot_bgcolor='rgb(275, 270, 273)')
    covid_fig.update_layout(paper_bgcolor='#111111')
    covid_fig.update_layout(plot_bgcolor='#111111')
    covid_fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    return covid_fig


@app.callback(
    dash.dependencies.Output('vaccine', 'figure'),
    [dash.dependencies.Input('state', 'value')])
def update_vac_graph(state):
    temp = date_wise_vaccine_data.copy()
    vac_fig = go.Figure(data=[
        go.Bar(name='Second Dose', x=temp['Updated On'], y=secounddose[state], marker_color='#2bad57'),
        go.Bar(name='First Dose', x=temp['Updated On'], y=firstdose[state], marker_color='#326ac7')])
    vac_fig.update_layout(barmode='stack')
    vac_fig.update_traces(textposition='inside')
    vac_fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    vac_fig.update_layout(title_text='COVID-19 Vaccine in ' + state,
                          font=dict(color='#7FDBFF'),
                          plot_bgcolor='rgb(275, 270, 273)')
    vac_fig.update_layout(paper_bgcolor='#111111')
    vac_fig.update_layout(plot_bgcolor='#111111')

    return vac_fig


if __name__ == "__main__":
    app.run_server(debug=True)
