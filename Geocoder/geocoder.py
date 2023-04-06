# from yandex_geocoder import Client
import base64
import io
import json
import requests
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
# import plotly.graph_objects as go
# import plotly.figure_factory as ff
import pandas as pd

def geocode(query):
    # coordinates = client.coordinates(query)
    response = requests.get(f'https://nominatim.openstreetmap.org/search?q={query.replace(" ", "+")}&format=json').json()
    for i in range(len(response)):
        response[i]['name'] = query
    return response

def get_coords_places(places):
    result = []
    for i in places:
        result.extend(geocode(i))
    return pd.DataFrame(result)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
px.set_mapbox_access_token('pk.eyJ1IjoieXVwZXN0IiwiYSI6ImNqdWpwOTJ6ZTA5MmQzeW1xeGdrb3VhcjkifQ.UEEIc5yM8s1lfMaREu-p6Q')


body = html.Div([
    html.H1("Геокодер"), 

    dbc.Row(
        dbc.Col(dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select File')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False))
    ),
    dbc.Row([html.Div(id='output-data-upload')]),
    dbc.Row([html.Button("Download CSV", id="btn-csv"),
             dcc.Download(id="download-dataframe-csv"),]),
    dbc.Row([html.Div(id = "output-map")]),
    dcc.Store(id='intermediate-value')
    
    ])
app.layout = html.Div([body])

def parse_contents(contents, filename):
    df_uploaded = pd.DataFrame()
    
    if contents:
        try:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)

            if 'csv' in filename:
                # Assume that the user uploaded a CSV file
                df_uploaded = pd.read_csv(
                    io.StringIO(decoded.decode('utf-8')))
            elif 'xls' in filename:
                # Assume that the user uploaded an excel file
                df_uploaded = pd.read_excel(io.BytesIO(decoded))
        except Exception as e:
            print(e)
            
    return df_uploaded

@app.callback(Output('output-map', 'children'),
              Input('intermediate-value', 'data'), prevent_initial_call=True)
def update_map(data):
    dataset = json.loads(data)
    dff = pd.read_json(dataset, orient='split')
    figure = px.scatter_mapbox(dff, lat="lat", lon="lon", hover_name = dff['name'], size_max=30,  zoom=10)
    figure.update_layout(margin=dict(b=0, t=0, l=0, r=0))
    children = dcc.Graph(id = 'map', figure = figure)
    return children

@app.callback(Output('download-dataframe-csv', 'data'),
              Input('btn-csv', "n_clicks"),
              State('intermediate-value', 'data'), prevent_initial_call=True)
def download_data(n_clicks, data):
    # print(data)
    dataset = json.loads(data)
    dff = pd.read_json(dataset, orient='split')
    return dcc.send_data_frame(dff.to_csv, "data.csv")

@app.callback(Output('output-data-upload', 'children'),
              Input('intermediate-value', 'data'), prevent_initial_call=True)
def update_output(data):
    dataset = json.loads(data)
    df = pd.read_json(dataset, orient='split')
    components = [
            # html.H5(filename),
            dash_table.DataTable(
                df.to_dict('records'),
                [{'name': i, 'id': i} for i in df.columns], 
                page_size = 15,
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                }
            ),

            html.Hr(),  # horizontal line
        ]

    children = html.Div(components)
    return children  
    
@app.callback(Output('intermediate-value', 'data'),
              Input('upload-data', 'contents'),
              Input('upload-data', 'filename'), prevent_initial_call=True)
#               State('upload-data', 'last_modified'))
def set_data(contents, filename):

    df = parse_contents(contents, filename)
    try:
        dff = get_coords_places(df['name']).drop(columns = ['icon', 'licence'])
        dff = df.merge(dff, how = 'left', on = 'name')
        dff['boundingbox'] = dff['boundingbox'].astype(str)
        dataset = dff.to_json(orient='split', date_format='iso')
        return json.dumps(dataset)
    except:
        pass
    
if __name__ == "__main__":
    app.run_server(debug = True, use_reloader=False)