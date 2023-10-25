import base64
import io
import json
import plotly.express as px
import dash
import numpy as np
from dash.dependencies import Input, Output
from dash import dcc, html, dash_table
import dash_daq as daq
import pandas as pd
import dash_draggable
import dash_bootstrap_components as dbc
from dash_holoniq_wordcloud import DashWordcloud

# ZOOM = {
#     'zoom': '80%'
# }

INPUT_STYLE = {
     'width': '100%'
}

P_STYLE = {
     'margin-top': 10,
     'margin-bottom': 5
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN], suppress_callback_exceptions=True)

app.layout = html.Div([
    dbc.Row([
        dbc.Col([

            html.Img(src ='https://github.com/yupest/nto/blob/master/src/Junior_full%20horiz.png?raw=true', width = '250px', style = {'margin-left': 14,'margin-top':14})

        ], width={'size':3}),

        dbc.Col([
            html.H1("НТО.Визуализация", style={'textAlign': 'left', 'margin-top': 7, 'margin-bottom': 7}),
        ], width={'size':8, 'offset':1})
    ]),
    # dcc.Dropdown(id='index', style = {'visibility':'hidden'}),
    dcc.Tabs([

        dcc.Tab(label='Данные', children = [

            dcc.Upload(
                id='upload-data',
                children=html.Div(['Перетащите или ', html.A('выберите файл')]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin-top': '10px'
                },
                multiple=False
            ),

            dcc.Store(id='data-file', storage_type='local'),
            html.Div(id='sort-data'),
            html.Div(id='output-datatable'),

        ]),

        dcc.Tab(label='Визуализация', children = [

            dcc.Tabs([
                dcc.Tab(label='Столбчатая диаграмма', children = [
                    dbc.Container([

                        dbc.Row([
                            dbc.Col([

                                html.Div(id='output-axis_1')

                            ], width={'size':3}),

                            dbc.Col([
                                html.Div(id='barchart-div-dupl'),
                            ], width={'size':8, 'offset':1})
                        ]),

                    ], fluid=True)
                ]),

                dcc.Tab(label='Линейная диаграмма', children = [
                    dbc.Container([

                        dbc.Row([

                            dbc.Col([
                                html.Div(id='output-axis_2'),
                            ], width={'size':3}),

                            dbc.Col([
                                html.Div(id='linechart-div-dupl'),
                            ], width={'size':8, 'offset':1})

                        ]),
                    ], fluid=True)
                ]),

                dcc.Tab(label='Точечная диаграмма', children = [
                    dbc.Container([

                        dbc.Row([

                            dbc.Col([
                                html.Div(id='output-axis_3'),
                            ], width={'size':3}),

                            dbc.Col([
                                html.Div(id='dotchart-div-dupl'),
                            ], width={'size':8, 'offset':1})

                        ]),
                    ], fluid=True)
                ]),

                dcc.Tab(label='Круговая диаграмма', children = [
                    dbc.Container([

                        dbc.Row([

                            dbc.Col([
                                html.Div(id='output-axis_4'),
                            ], width={'size':3}),

                            dbc.Col([
                                html.Div(id='piechart-div-dupl'),
                            ], width={'size':8, 'offset':1})

                        ]),
                    ], fluid=True)
                ]),

                dcc.Tab(label='Облако слов', children = [
                    dbc.Container([

                        dbc.Row([

                            dbc.Col([
                                html.Div(id='output-worcloud'),
                            ], width={'size':3}),

                            dbc.Col([
                                html.Div(id='wordcloud-div-dupl'),
                            ], width={'size':5, 'offset':1}),
                            dbc.Col([
                                html.Div(id='color-picker'),
                            ], width={'size':3})

                        ]),
                    ], fluid=True)
                ]),

                dcc.Tab(label='Текст', children = [
                    dbc.Container([

                        dbc.Row([
                            dbc.Col([
                                dcc.Input(id = 'input-name-dashboard',
                                          type = 'text',
                                          placeholder = 'Название Дашборда',
                                          style = INPUT_STYLE,
                                          persistence='local'),
                                html.P("Размер текста", style = P_STYLE),
                                dcc.Slider(min=6, max=24, step=1, value=14, id='text-size-slider', marks=None,
                                    tooltip={"placement": "bottom", "always_visible": True}, persistence='local')

                            ], width={'size':3}),

                            dbc.Col([
                                dcc.Textarea(
                                    id='textarea-example',
                                    value='',
                                    style={'width': '100%', 'height': 400, 'resize': 'none', 'align':'top'},
                                    persistence='local',
                                ),
                            ], width={'size':8, 'offset':1})

                        ], style={'margin-top':20}),
                    ], fluid=True)
                ]),

            ]),
        ]),

        dcc.Tab(label='Дашборд', children = [
            html.H3(id = 'name-dashboard', style={'textAlign': 'center', 'margin-top': 7}),
            dash_draggable.ResponsiveGridLayout([
                html.Div(id='barchart-div',
                         style={
                            "height":'100%',
                            "width":'100%',
                            "display":"flex",
                            "flex-direction":"column",
                            "flex-grow":"0"
                        }),
                html.Div(id='linechart-div',
                         style={
                            "height":'100%',
                            "width":'100%',
                            "display":"flex",
                            "flex-direction":"column",
                            "flex-grow":"0"
                        }),
                html.Div(id='dotchart-div',
                         style={
                            "height":'100%',
                            "width":'100%',
                            "display":"flex",
                            "flex-direction":"column",
                            "flex-grow":"0"
                        }),
                html.Div(id='piechart-div',
                         style={
                            "height":'100%',
                            "width":'100%',
                            "display":"flex",
                            "flex-direction":"column",
                            "flex-grow":"0"
                        }),
                html.Div(id='wordcloud-div',
                         style={
                            "height":'100%',
                            "width":'100%',
                            "display":"flex",
                            "flex-direction":"column",
                            "flex-grow":"0"
                        }),
                html.Div(id='textarea-example-output', style={'whiteSpace': 'pre-line', 'margin-left':15}),
            ],gridCols = {'lg': 16, 'md': 12, 'sm': 8, 'xs': 4, 'xxs': 2})
        ])
    ]),
])

######################################## processing the name dasboard ########################################
@app.callback(Output('name-dashboard', 'children'),
              Input('input-name-dashboard','value'))
def set_name_dashboard(name):
    return name

######################################## processing the data ########################################
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
                # Ase that the user uploaded an excel file
                df_uploaded = pd.read_excel(io.BytesIO(decoded))
            elif 'json' in filename:
                # Ase that the user uploaded an excel file
                df_uploaded = pd.read_json(io.StringIO(decoded.decode('utf-8')))

        except Exception as e:
            print('parse content ', e)

    return df_uploaded

@app.callback(Output('data-file', 'data'),
              Input('upload-data', 'contents'),
              Input('upload-data', 'filename'), prevent_initial_call=True)

def set_data(contents, filename):
    json_data = {'filename':filename}
    df = parse_contents(contents, filename)

    try:
        dataset = df.to_json(orient='split', date_format='iso')
        json_data['data'] = dataset
        return json.dumps(json_data)

    except Exception as e:
        print(e)
        return json.dumps(json_data)

######################################## processing the table ########################################
@app.callback(Output('output-datatable', 'children'),
              Input('data-file', 'data'),
              # Input('sort-column', 'value'),
              # Input('sort-type', 'value'),
              # Input('slice-slider', 'value'),
              prevent_initial_call=True)

def get_table(data):
    dataset = json.loads(data)

    if not '[]' in dataset['data']:
        df = pd.read_json(dataset['data'], orient='split')


        return [html.H3(dataset['filename'],
                        style = {'text-align': 'center',
                                 'margin-top': 15
                        }
                        ),

                dash_table.DataTable(
                    id = 'df-table',
                    data=df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns],

                    style_table={'overflowX': 'auto'},

                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable="single",
                    row_selectable="multi",
                    row_deletable=True,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    page_size=15
                ),

        ]
    else:
        return [html.P('Не удалось прочитать файл, доступные форматы: xls, xlsx, csv, json', style=P_STYLE)]


# @app.callback([Output('index', 'options'), Output('index', 'style')],
#               Input('data-file', 'data'),
#               prevent_initial_call=True)
# def set_index(data):
#     dataset = json.loads(data)['data']
#     df = pd.read_json(dataset, orient='split')

#     return [ [{'label':x, 'value':x} for x in df.columns], {'visibility':'visible'}]


######################################## processing the barchart ########################################
@app.callback(Output('output-axis_1', 'children'),
              Input('data-file', 'data'),
              prevent_initial_call=True)

def draw_bar(data):
    dataset = json.loads(data)['data']
    df = pd.read_json(dataset, orient='split')

    return [html.Div([
        html.P("Выберите ось X", style = P_STYLE),
        dcc.Dropdown(id='xaxis-data_1',
                     options=[{'label':x, 'value':x} for x in df.columns], persistence='local'),
        html.P("Выберите ось Y", style = P_STYLE),
        dcc.Dropdown(id='yaxis-data_1',
                     options=[{'label':x, 'value':x} for x in df.columns], multi=True, persistence='local'),
        html.P("Агрегация", style = P_STYLE),
        dcc.Dropdown(id='agg-data_1',
                     options={
                         'sum': 'Сумма',
                         'avg': 'Среднее',
                         'count': 'Количество',
                         'countd':'Количество уникальных',
                         'min': 'Минимум',
                         'max': 'Максимум',
                         },
                     value='sum',
                     persistence='local'),
        dcc.Checklist(options = {'h':'Горизонтальная диаграмма'}, id = 'orientation', persistence='local'),
        dcc.Checklist(options = {'top':'Создать топ'}, id = 'creation-top', persistence='local'),
        dcc.Slider(min=1, max=20, step=1, value=20, id='top-slider', marks=None, disabled = True,
                    tooltip={"placement": "bottom", "always_visible": True}, persistence='local'),
        html.P("Введите название графика", style = P_STYLE),
        dcc.Input(id="barchart-name", type="text", placeholder="Название", style = INPUT_STYLE, persistence='local'),
        # html.Hr()
        ]
    )]
@app.callback(Output('top-slider', 'disabled'),
              Input('creation-top', 'value'),
              prevent_initial_call=False)
def update_disabled_top_slider(value):
    return not value


@app.callback([Output('barchart-div-dupl', 'children'),
              Output('barchart-div', 'children')],
              [Input('data-file','data'),
              Input('xaxis-data_1','value'),
              Input('yaxis-data_1', 'value'),
              Input('agg-data_1', 'value'),
              Input('barchart-name','value'),
              Input('creation-top', 'value'),
              Input('top-slider', 'value'),
              Input('orientation', 'value')],
              prevent_initial_call=False)

def make_bar(data, x_data, y_data, agg_data, barchart_name, creation_top, top_slider, orientation):

        ### dictionary for an aggregation ###
        d = {'sum': 'sum()', 'avg':'mean()', 'count': 'count()', 'countd': 'nunique()', 'min':'min()', 'max':'max()'}

        dataset = json.loads(data)['data']
        df = pd.read_json(dataset, orient='split')

        nnn = df.groupby(x_data)[y_data]
        r = {'nnn':nnn}
        exec('nnn = nnn.'+d[agg_data], r)

        y_axis = agg_data+'('+y_data[0]+')' if len(y_data)==1 else 'value'

        o = None
        if orientation:
            o = 'h'
            df_temp = r['nnn'].sort_values(y_data, ascending = True)
            for y_col in y_data:
                df_temp = df_temp.loc[~df_temp[y_col].isna()]

            if creation_top:
                df_temp = df_temp.tail(top_slider)

            x = y_data[0] if len(y_data)==1 else y_data
            y = df_temp.index
        else:
            df_temp = r['nnn'].sort_values(y_data, ascending = False)

            if creation_top:
                df_temp = df_temp[:top_slider]

            x = df_temp.index
            y = y_data[0] if len(y_data)==1 else y_data

        bar_fig = px.bar(df_temp, x=x, y=y, labels={'y':y_axis,'x': x_data}, orientation = o)
        bar_fig.update_layout(
            title={
                'text': barchart_name,
                'y':0.94,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
            },
            # showlegend = False
            # height = 600
        )
        return dcc.Graph(figure=bar_fig), dcc.Graph(figure=bar_fig, responsive=True, style={"min-height":"0","flex-grow":"1"})

######################################## processing the linechart ########################################
@app.callback(Output('output-axis_2', 'children'),
              Input('data-file', 'data'),
              prevent_initial_call=True)

def draw_line(data):
    dataset = json.loads(data)['data']
    df = pd.read_json(dataset, orient='split')
    return [html.Div([
        html.P("Выберите ось X", style = P_STYLE),
        dcc.Dropdown(id='xaxis-data_2',
                     options=[{'label':x, 'value':x} for x in df.columns], persistence='local'),
        html.P("Выберите ось Y", style = P_STYLE),
        dcc.Dropdown(id='yaxis-data_2',
                     options=[{'label':x, 'value':x} for x in df.columns], multi=True, persistence='local'),
        html.P("Агрегация", style = P_STYLE),
        dcc.Dropdown(id='agg-data_2',
                     options={
                         'sum': 'Сумма',
                         'avg': 'Среднее',
                         'count': 'Количество',
                         'countd':'Количество уникальных',
                         'min': 'Минимум',
                         'max': 'Максимум',
                         },
                     value='sum',
                     persistence='local'),
        html.P("Введите название графика", style = P_STYLE),
        dcc.Input(id="linechart-name", type="text", placeholder="Название", style = INPUT_STYLE, persistence='local'),
        ]
    )]

@app.callback([Output('linechart-div-dupl', 'children'),
               Output('linechart-div', 'children')],
              [Input('data-file','data'),
              Input('xaxis-data_2','value'),
              Input('yaxis-data_2', 'value'),
              Input('agg-data_2', 'value'),
              Input('linechart-name','value')],
              prevent_initial_call=False)

def make_line(data, x_data, y_data, agg_data, linechart_name):

        ### dictionary for an aggregation ###
        d = {'sum': 'sum()', 'avg':'mean()', 'count': 'count()', 'countd': 'nunique()', 'min':'min()', 'max':'max()'}

        dataset = json.loads(data)['data']
        df = pd.read_json(dataset, orient='split')

        nnn = df.groupby(x_data)[y_data]
        r = {'nnn':nnn}
        exec('nnn = nnn.'+d[agg_data], r)

        line_fig = px.line(r['nnn'], x=r['nnn'].index, y=y_data, color_discrete_sequence=px.colors.qualitative.Plotly)
        line_fig.update_layout(
            title={
                'text': linechart_name,
                'y':0.94,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        return dcc.Graph(figure=line_fig), dcc.Graph(figure=line_fig, responsive=True, style={"min-height":"0","flex-grow":"1"})

######################################## processing the dotchart ########################################
@app.callback(Output('output-axis_3', 'children'),
              Input('data-file', 'data'),
              prevent_initial_call=True)

def draw_scatter(data):
    dataset = json.loads(data)['data']
    df = pd.read_json(dataset, orient='split')
    return [html.Div([
        html.P("Выберите ось X", style = P_STYLE),
        dcc.Dropdown(id='xaxis-data_3',
                     options=[{'label':x, 'value':x} for x in df.columns], persistence='local'),
        html.P("Выберите ось Y", style = P_STYLE),
        dcc.Dropdown(id='yaxis-data_3',
                     options=[{'label':x, 'value':x} for x in df.columns], persistence='local'),
        html.P("Настройка подсказки", style = P_STYLE),
        dcc.Dropdown(id='tooltip-dot', multi=True,
                     options=[{'label':x, 'value':x} for x in df.columns], persistence='local'),
        html.P("Выберите размер", style = P_STYLE),
        dcc.Dropdown(id='size-data_3',
                     options=[{'label':x, 'value':x} for x in df.columns], persistence='local'),
        html.P("Выберите цвет", style = P_STYLE),
        dcc.Dropdown(id='color-data_3',
                     options=[{'label':x, 'value':x} for x in df.columns], persistence='local'),
        html.P("Введите название графика", style = P_STYLE),
        dcc.Input(id="dotchart-name", type="text", placeholder="Название", style = INPUT_STYLE, persistence='local'),
        ]
    )]

@app.callback([Output('dotchart-div-dupl', 'children'),
               Output('dotchart-div', 'children')],
              [Input('data-file','data'),
              Input('xaxis-data_3','value'),
              Input('yaxis-data_3', 'value'),
              Input('tooltip-dot', 'value'),
              Input('size-data_3', 'value'),
              Input('color-data_3', 'value'),
              Input('dotchart-name','value')],
              prevent_initial_call=False)

def make_scatter(data,  x_data, y_data, tooltip, size_data, color_data, dotchart_name):
        dataset = json.loads(data)['data']
        df = pd.read_json(dataset, orient='split')

        cols = tooltip
        for i in [x_data, y_data, size_data, color_data]:
            if not pd.isna(i):
                cols.append(i)
                df = df.loc[~df[i].isna()]


        dot_fig = px.scatter(df, x=x_data, y=y_data, size=size_data, hover_data=cols,
                             color_discrete_sequence=px.colors.qualitative.Plotly, color=color_data)
        dot_fig.update_layout(
            title={
                'text': dotchart_name,
                'y':0.94,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        return dcc.Graph(figure=dot_fig), dcc.Graph(figure=dot_fig, responsive=True, style={"min-height":"0","flex-grow":"1"})

######################################## processing the piechart ########################################
@app.callback(Output('output-axis_4', 'children'),
              Input('data-file', 'data'),
              prevent_initial_call=True)

def draw_pie(data):
    dataset = json.loads(data)['data']
    df = pd.read_json(dataset, orient='split')
    return [html.Div([
        html.P("Выберите метки", style = P_STYLE),
        dcc.Dropdown(id='xaxis-data_4',
                     options=[{'label':x, 'value':x} for x in df.columns], persistence='local'),
        html.P("Выберите секторы", style = P_STYLE),
        dcc.Dropdown(id='yaxis-data_4',
                     options=[{'label':x, 'value':x} for x in df.columns], persistence='local'),
        html.P("Количество уникальных секторов", style = P_STYLE),
        dcc.Slider(min=1, max=20, step=1, value=7, id='sectors-slider', marks=None,
                    tooltip={"placement": "bottom", "always_visible": True}, persistence='local'),
        html.P("Агрегация", style = P_STYLE),
        dcc.Dropdown(id='agg-data_3',
                     options={
                         'sum': 'Сумма',
                         'avg': 'Среднее',
                         'count': 'Количество',
                         "countd":'Количество уникальных',
                         'min': 'Минимум',
                         'max': 'Максимум',
                         },
                     value='sum',
                     persistence='local'),
        html.P("Введите название графика", style = P_STYLE),
        dcc.Input(id="piechart-name", type="text", placeholder="Название", style = INPUT_STYLE, persistence='local'),
        ]
    )]

@app.callback([Output('piechart-div-dupl', 'children'),
               Output('piechart-div', 'children')],
              [Input('data-file','data'),
              Input('xaxis-data_4','value'),
              Input('yaxis-data_4', 'value'),
              Input('sectors-slider', 'value'),
              Input('agg-data_3', 'value'),
              Input('piechart-name','value')],
              prevent_initial_call=False)

def make_pie(data, x_data, y_data, sliderSectors, agg_data, piechart_name):

        ### dictionary for an aggregation ###
        d = {'sum': 'sum()', 'avg':'mean()', 'count': 'count()', 'countd': 'nunique()', 'min':'min()', 'max':'max()'}

        dataset = json.loads(data)['data']
        df = pd.read_json(dataset, orient='split')

        df_temp = df[[x_data, y_data]].groupby(by=x_data)
        r = {'df_temp':df_temp}
        exec('df_temp = df_temp.'+d[agg_data], r)

        df_temp = r['df_temp']

        if df_temp.shape[0] > sliderSectors:
             df_temp = df_temp.sort_values(y_data, ascending = False).reset_index()
             df_temp.loc[sliderSectors:, x_data] = 'Другое'
             df_temp = df_temp.groupby(x_data).sum()

        pie_fig = px.pie(df_temp, values=y_data, names=df_temp.index, color_discrete_sequence=px.colors.qualitative.Plotly)
        pie_fig.update_layout(
            title={
                'text': piechart_name,
                'y':0.94,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )

        pie_fig.update_traces(
             textposition="inside",
             textinfo='percent+label'

        )

        return dcc.Graph(figure=pie_fig), dcc.Graph(figure=pie_fig, responsive=True, style={"min-height":"0","flex-grow":"1"})

######################################## processing the text ########################################
# @app.callback([Output('output-worcloud', 'children'),
#                Output('color-picker', 'children')],
#               Input('data-file', 'data'),
#               prevent_initial_call=True)

# def set_worcloud(data):
#     dataset = json.loads(data)['data']
#     df = pd.read_json(dataset, orient='split')
#     return [html.Div([
#                 html.P("Минимальная длина слова", style = P_STYLE),
#                 dcc.Slider(min=1, max=5, step=1, value=3, id='lenth-slider', marks=None,
#                             tooltip={"placement": "bottom", "always_visible": True}, persistence='local')
#                 ])
#            ]

@app.callback(Output('textarea-example-output', 'children'),
        Input('textarea-example', 'value'),
        Input('text-size-slider', 'value')
    )
def update_output(text, size):
    return html.P(format(text),
        style = {
            'font-size': size,
        }
    )

######################################## processing the wordcloud ########################################
@app.callback([Output('output-worcloud', 'children'),
               Output('color-picker', 'children')],
              Input('data-file', 'data'),
              prevent_initial_call=True)

def set_worcloud(data):
    dataset = json.loads(data)['data']
    df = pd.read_json(dataset, orient='split')
    return [html.Div([
                html.P("Выберите данные", style = P_STYLE),
                dcc.Dropdown(id='worcloud_column',
                            options=df.columns[np.array([df[i].dtype == 'object' for i in df.columns])].tolist(),
                            persistence='local'),
                html.P("Подсчет количества уникальных по полю:", style = P_STYLE),
                dcc.Dropdown(id='worcloud_count',
                            options=df.columns,
                            persistence='local'),
                html.P("Минимальная длина слова", style = P_STYLE),
                dcc.Slider(min=1, max=5, step=1, value=3, id='lenth-slider', marks=None,
                            tooltip={"placement": "bottom", "always_visible": True}, persistence='local'),
                html.P("Частота упоминаний от", style = P_STYLE),
                dcc.Slider(min=1, max=10, step=1, value=3, id='frequency-slider', marks=None,
                            tooltip={"placement": "bottom", "always_visible": True}, persistence='local'),
                html.P("Размер слов", style = P_STYLE),
                dcc.Slider(min=1, max=5, step=0.5, value=1, id='size-slider', marks=None,
                            tooltip={"placement": "bottom", "always_visible": True}, persistence='local'),
                # html.P("Высота", style = P_STYLE),
                # dcc.Slider(min=200, max=1000, step=50, value=500, id='height-slider', marks=None,
                #             tooltip={"placement": "bottom", "always_visible": True}, persistence='local'),
                html.P("Сетка", style = P_STYLE),
                dcc.Slider(min=3, max=25, step=1, value=15, id='grid-slider', marks=None,
                            tooltip={"placement": "bottom", "always_visible": True}, persistence='local'),

                ]
        # dcc.Textarea(id = 'result')]
            ),
            html.Div([
                html.P("Выберите цвет", style = P_STYLE),
                daq.ColorPicker(
                id='words-color',
                value=dict(hex='#000000'),
                # size=200,
                persistence='local',
                style={'border':'0px'},
            )], style={'height':500, 'margin-top':10})
    ]

@app.callback([Output('wordcloud-div-dupl', 'children'),
               Output('wordcloud-div', 'children'),
               Output('frequency-slider', 'max')],
              [Input('data-file', 'data'),
              Input('worcloud_column', 'value'),
              Input('worcloud_count', 'value'),
              Input('lenth-slider', 'value'),
              Input('size-slider', 'value'),
              # Input('height-slider', 'value'),
              Input('grid-slider', 'value'),
              Input('words-color', 'value'),
              Input ('frequency-slider', 'value')],
              prevent_initial_call=True)

def draw_wordcloud(data, column, column_count, sliderLength, slider_size, sliderGrid, wordsColor, frequency):
    security_data = []

    dataset = json.loads(data)['data']
    df = pd.read_json(dataset, orient='split')

    try:

        if column_count:
            df = df[[column, column_count]].drop_duplicates()

        words = df[column].str.upper().str.extractall(r'([A-ZА-ЯЁ\d\-]+)').reset_index('match')
        words['lenth'] = words[0].apply(len)
        df_temp = words.loc[words['lenth']>=sliderLength, 0].value_counts()
        mx, mn = df_temp.values.max(), df_temp.values.min()
        security_data = [[k, ((x-mn)/ (mx-mn))*(25)+5, k+' ('+str(x)+')'] for k, x in zip(df_temp.keys(), df_temp.values) if x >= frequency]

        origin_data = [[k, v] for k, v in df_temp.items() if v >= frequency]

    except:
        pass

    cloud = DashWordcloud(
            id='wordcloud',
            list=security_data,
            width=500, height=500,
            gridSize=sliderGrid,
            weightFactor=slider_size,
            # weightFactor = 3,
            color=wordsColor['hex'],
            backgroundColor='#fff',
            shuffle=False,
            rotateRatio=0.5,
            # shrinkToFit=True,
            # shape='square',
            ellipticity=1,
            hover=True,
            # minSize = 16,
            # origin = [10,10]
        )

    return cloud, cloud, security_data[0][1]


# running the server
if __name__ == '__main__':
    app.run_server(debug=True)