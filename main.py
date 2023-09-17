import requests
from basic_iss import *
from dash import Dash, html, dcc
import plotly.express as px
from dash.dependencies import Input, Output
import datetime

app = Dash(__name__)

get_iss_location()

lat_long = {
    'latitude': [],
    'longitude': []
}

fig = px.line_geo()
fig.update_geos(projection_type="natural earth")
fig.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})

app.layout = html.Div([
    html.H1('ISS Location Tracker', style={'color': 'white'}),
    html.Div(id='lat-long-text', style={'color': 'white'}),
    dcc.Graph(id='map', figure=fig),
    dcc.Interval(
            id='interval-component',
            interval=1000, # in milliseconds
            n_intervals=0
        )
], style={'text-align': 'center', 'backgroundColor': '#333333', 'padding': '20px'})

@app.callback(Output('lat-long-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_lat_long_text(interval):
    iss_location = get_iss_location()
    latitude = iss_location[0]
    longitude = iss_location[1]

    # Get current time in UTC and IST
    utc_time = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    ist_time = (datetime.datetime.utcnow() + datetime.timedelta(hours=5, minutes=30)).strftime('%Y-%m-%d %H:%M:%S IST')

    
    style = {'padding': '10px', 'fontSize': '22px'}

    

    return [
        html.Span('Latitude: {}'.format(latitude), style=style),
        html.Span('Longitude: {}'.format(longitude), style=style),
        html.Span(utc_time, style={'color': 'white', 'padding-right': '10px'}),
        html.Span(ist_time, style={'color': 'white'})
    ]

@app.callback(Output('map', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_map(interval):
    iss_location = get_iss_location()

    lat_long['latitude'].append(iss_location[0])
    lat_long['longitude'].append(iss_location[1])
    
    fig = px.line_geo(lat=lat_long['latitude'], lon=lat_long['longitude'])
    fig.update_geos(projection_type="natural earth")
    fig.update_layout(height=500, margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_traces(line=dict(color="Red", width=4))

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)