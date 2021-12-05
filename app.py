import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from datetime import date
from datetime import datetime

app = Dash(__name__)

# -- Import and clean data (importing csv into pandas)

# Reading vaccine data and covid cases data and strong them in vaccine_data and df resprectively
df = pd.read_csv("covid_19_india.csv")
vaccine_data=pd.read_csv('covid_vaccine_statewise.csv')
# vaccine_data['Updated On']=datetime.strptime(str(vaccine_data['Updated On']),"%d/%m/%Y").strftime("%Y-%m-%d")
print(vaccine_data)
for col in df.columns:
    df[col] = df[col].astype(str)

for col in vaccine_data.columns:
    vaccine_data[col] = vaccine_data[col].astype(str)

# adding a column known as text which will show the data on hover on the map

df['text'] = 'Confirmed Cases :- ' + df['Confirmed'] + '<br>' + 'Death Cases :- ' + df['Deaths'] + '<br>' + 'Cured Cases :- ' + df['Cured'] + '<br>'
vaccine_data['text'] = 'Total Doses Administered :- ' + vaccine_data['Total Doses Administered'] + '<br>' + 'Sessions :- ' + vaccine_data['Sessions'] + '<br>' + 'Male (Doses Administered) :- ' + vaccine_data['Male (Doses Administered)'] + '<br>' + 'Female (Doses Administered) :- ' + vaccine_data['Female (Doses Administered)'] + '<br>' + 'Transgender (Doses Administered) :- ' + vaccine_data['Transgender (Doses Administered)'] + '<br>'
# ------------------------------------------------------------------------------
# App layout
# this is the layout of the webpage i.e our dashboard
app.layout = html.Div([
# Heading
    html.H1("Covid-19 Dashboards with Indian Dataset", style={'text-align': 'center'}),
# Date Picker and graph
    html.Div(
        children=[
            html.Div(
        children=[
            dcc.DatePickerSingle(
        id='my-date-picker-single',
        min_date_allowed=date(2019, 8, 5),
        max_date_allowed=date(2021, 8, 11),
        initial_visible_month=date(2021, 8,7),
        date=date(2021, 8, 7)
    ),

            html.Div(id='output-container-date-picker-single', children=[]),
            html.Br(),

            dcc.Graph(id='my_bee_map', figure={}),
        ],style={ 'flex': 1}
    ),
    html.Div(
        children=[
            dcc.DatePickerSingle(
        id='my-date-picker-single2',
        min_date_allowed=date(2019, 8, 5),
        max_date_allowed=date(2021, 8, 11),
        initial_visible_month=date(2021, 8,7),
        date=date(2021, 6, 4)
    ),

    html.Div(id='output-container-date-picker-single2', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map2', figure={}),
        ],style={'flex': 1}
    ),
        ]
        ,style={'display': 'flex', 'flex-direction': 'row'}
    )
])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
# This is basically the calllback to connect the Dash Component and Dash Graph with each other
@app.callback(
    [Output('output-container-date-picker-single', 'children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input('my-date-picker-single', 'date')]
)
# the funnction that will trigeer on the value change in date picker
def update_graph(date_value):
    print(date_value)
    string_prefix = 'Showing Results of : '
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')
        container = string_prefix + date_string
    dff = df.copy()
    # getting alll the datat at that selected date
    dff = dff[dff["Date"] == date_value]
    print(dff)
    # here we are making the map of indaia using GeoLoca because its on available on PLotly only US map is avaialble
    fig = go.Figure(data=go.Choropleth(
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locationmode='geojson-id',
    locations=dff['State/UnionTerritory'],
    z=dff['Confirmed'],
    text=dff['text'],

    autocolorscale=False,
    colorscale=["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
      "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
      "#08519c", "#0b4083", "#08306b"
    ],
    marker_line_color='peachpuff',
    ))
    fig.update_geos(
      visible=False,
      projection=dict(
        type='conic conformal',
        parallels=[12.472944444, 35.172805555556],
        rotation={'lat': 24, 'lon': 80}
      ),
      lonaxis={'range': [68, 98]},
      lataxis={'range': [6, 38]}
    )
    fig.update_layout(
         title=dict(
        text="Active COVID-19 Cases in India by State",
        xanchor='center',
        x=0.5,
        yref='paper',
        yanchor='bottom',
        y=1,
        pad={'b': 10}
    ),
      margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
      height=550,
      width=450
    )
    return container, fig
#  callback function for vaccination data

@app.callback(
    [Output('output-container-date-picker-single2', 'children'),
     Output(component_id='my_bee_map2', component_property='figure')],
    [Input('my-date-picker-single2', 'date')]
)
def update_graph(date_value):
    print(date_value)
    string_prefix = 'Showing Results of : '
    if date_value is not None:
        date_object = date.fromisoformat(date_value)
        date_string = date_object.strftime('%B %d, %Y')
        container = string_prefix + date_string
    dff = vaccine_data.copy()
    date_value=datetime.strptime(date_value, "%Y-%m-%d").strftime("%d/%m/%Y")
    print(date_value)
    dff = dff[dff["Updated On"] == date_value]
    print(dff)
    fig = go.Figure(data=go.Choropleth(
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locationmode='geojson-id',
    locations=dff['State'],
    z=dff['Total Individuals Vaccinated'],
    text=dff['text'],

    autocolorscale=False,
    colorscale=["#f7fbff", "#ebf3fb", "#deebf7", "#d2e3f3", "#c6dbef", "#b3d2e9", "#9ecae1",
      "#85bcdb", "#6baed6", "#57a0ce", "#4292c6", "#3082be", "#2171b5", "#1361a9",
      "#08519c", "#0b4083", "#08306b"
    ],
    marker_line_color='peachpuff',
    ))
    fig.update_geos(
      visible=False,
      projection=dict(
        type='conic conformal',
        parallels=[12.472944444, 35.172805555556],
        rotation={'lat': 24, 'lon': 80}
      ),
      lonaxis={'range': [68, 98]},
      lataxis={'range': [6, 38]}
    )
    fig.update_layout(
         title=dict(
        text="COVID-19 Vaccination Status in India by State",
        xanchor='center',
        x=0.5,
        yref='paper',
        yanchor='bottom',
        y=1,
        pad={'b': 10}
    ),
      margin={'r': 0, 't': 30, 'l': 0, 'b': 0},
      height=550,
      width=450
    )
    return container, fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
