from flask import Flask
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dash_table
import plotly.graph_objs as go
from functools import reduce
external_stylesheets = [dbc.themes.MINTY]

server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

students = [['Kinora', 18, 'Buchs ZH', 'BM21b'],
            ['Zarin', 17, 'Oerlikon', 'IA21b'],
            ['Elina', 17, 'Oerlikon', 'IA21a'],
            ['Elena', 17, 'Schlieren', 'BM21b'],
            ['Mischa', 18, 'Winterthur', 'IA21b'],
            ['Mattia', 17, 'Winterthur', 'BM21b'],
            ['Robin', 18, 'Oetwil an der Limmat', 'BM21b'],
            ['Jenaya', 18, 'Greifensee', 'BM21b']]

grades = [['Kinora', 5.6, 'Englisch'],
          ['Kinora', 4.8, 'Deutsch'],
          ['Kinora', 5.3, 'Französisch'],
          ['Kinora', 5.5, 'Englisch'],
          ['Kinora', 5.8, 'Englisch'],
          ['Kinora', 5.6, 'Deutsch'],
          ['Zarin', 6, 'Englisch'],
          ['Zarin', 5, 'Deutsch'],
          ['Zarin', 4.6, 'Französisch'],
          ['Zarin', 5.1, 'Englisch'],
          ['Zarin', 5.7, 'Englisch'],
          ['Zarin', 5.1, 'Deutsch'],
          ['Zarin', 5.5, 'Deutsch'],
          ['Zarin', 4.8, 'Französisch'],
          ['Zarin', 4.6, 'Französisch'],
          ['Elina', 5.1, 'Englisch'],
          ['Elina', 4.9, 'Englisch'],
          ['Elina', 5.9, 'Deutsch'],
          ['Elina', 5.9, 'Deutsch'],
          ['Elina', 4.7, 'Französisch'],
          ['Elina', 4.8, 'Französisch'],
          ['Elina', 5.7, 'Englisch'],
          ['Elina', 4.5, 'Deutsch'],
          ['Elina', 5.5, 'Französisch'],
          ['Mischa', 5.7, 'Englisch'],
          ['Mischa', 5, 'Deutsch'],
          ['Mischa', 5, 'Französisch'],
          ['Mattia', 5, 'Englisch'],
          ['Mattia', 4.5, 'Deutsch'],
          ['Mattia', 5, 'Französisch'],
          ['Mattia', 5.4, 'Englisch'],
          ['Mattia', 5.6, 'Englisch'],
          ['Mattia', 5.3, 'Deutsch'],
          ['Mattia', 4.5, 'Deutsch'],
          ['Mattia', 4.6, 'Französisch'],
          ['Mattia', 5.8, 'Französisch'],
          ['Jenaya', 4.8, 'Englisch'],
          ['Jenaya', 5, 'Deutsch'],
          ['Jenaya', 5.3, 'Französisch'],
          ['Jenaya', 4.8, 'Englisch'],
          ['Jenaya', 5.9, 'Englisch'],
          ['Jenaya', 4.6, 'Deutsch'],
          ['Jenaya', 4.8, 'Deutsch'],
          ['Jenaya', 5.8, 'Französisch'],
          ['Jenaya', 5.2, 'Französisch'],
          ['Robin', 4.6, 'Englisch'],
          ['Robin', 5.6, 'Deutsch'],
          ['Robin', 5.6, 'Französisch'],
          ['Robin', 4.6, 'Englisch'],
          ['Robin', 5.6, 'Deutsch'],
          ['Robin', 5.6, 'Französisch'],
          ['Robin', 5.2, 'Englisch'],
          ['Robin', 4.7, 'Deutsch'],
          ['Robin', 5.1, 'Französisch'],
          ['Mischa', 5.0, 'Englisch'],
          ['Mischa', 4.5, 'Deutsch'],
          ['Mischa', 5.0, 'Französisch'],
          ['Mischa', 5.0, 'Englisch'],
          ['Mischa', 4.5, 'Deutsch'],
          ['Mischa', 5.0, 'Französisch'],
          ['Elena', 5.7, 'Englisch'],
          ['Elena', 5, 'Deutsch'],
          ['Elena', 5, 'Französisch'],
          ['Elena', 5.4, 'Englisch'],
          ['Elena', 4.8, 'Englisch'],
          ['Elena', 5.7, 'Deutsch'],
          ['Elena', 5.9, 'Deutsch'],
          ['Elena', 5.7, 'Französisch'],
          ['Elena', 5.7, 'Französisch']]

studentdf = pd.DataFrame(students, columns=['Name', 'Alter', 'Stadt', 'Klasse'])
gradedf = pd.DataFrame(grades, columns=['Name', 'Note', 'Fach'])


def categorize_grade(grade):
    if grade >= 5.5:
        return "Sehr Gut"
    elif grade >= 4.5:
        return "Gut"
    elif grade >= 3.5:
        return "Befriedigend"
    else:
        return "Nicht Ausreichend"

gradedf['NotenKategorie'] = list(map(categorize_grade, gradedf['Note']))


englisch_grades = list(filter(lambda x: x['Fach'] == 'Englisch', gradedf.to_dict('records')))


total_grade_sum = reduce(lambda x, y: x + y, gradedf['Note'], 0)
average_total_grade = total_grade_sum / len(gradedf)


gradedf['Note'] = gradedf['Note'].round(1)

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-students', children=[
        dcc.Tab(label='Students', value='tab-students'),
        dcc.Tab(label='Grades', value='tab-grades'),
    ], colors={
        "border": "black",
        "primary": "black",
        "background": "white"
    }),
    html.Div(id='tabs-content')
], style={'backgroundColor': 'white'})


def filter_grade(subject):
    return lambda row: row['Fach'] == subject


def average_grade(grades_list):
    return sum(grades_list) / len(grades_list)


app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-students', children=[
        dcc.Tab(label='Students', value='tab-students'),
        dcc.Tab(label='Grades', value='tab-grades'),
    ]),
    html.Div(id='tabs-content')
])


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-students':
        return html.Div([
            dash_table.DataTable(
                id='table-students',
                columns=[{"name": i, "id": i} for i in studentdf.columns],
                data=studentdf.to_dict('records'),
            )
        ])
    elif tab == 'tab-grades':
        return html.Div([
            html.H4('Filter by name', style={'color': 'black'}),
            dcc.Dropdown(
                id='name-dropdown',
                options=[{'label': name, 'value': name} for name in gradedf['Name'].unique()],
                value=gradedf['Name'].unique()[0],
                style={'backgroundColor': 'white', 'color': 'black'}
            ),
            dcc.Graph(id='grades', style={'color': 'white'}),
            html.H4(f'Durchschnittsnote aller Schüler: {average_total_grade:.2f}'),
            html.Div(id='average')
        ], style={'backgroundColor': 'white', 'color': 'black'})

@app.callback(
    [Output('grades', 'figure'),
     Output('average', 'children')],
    [Input('name-dropdown', 'value')]
)
def update_content(selected_name):
    if selected_name:
        filtered_df = gradedf[gradedf['Name'] == selected_name]
        fig = px.pie(filtered_df, names='Fach', values='Note', title=f"Notenverteilung für {selected_name}")
        fig.update_layout(paper_bgcolor='white', font_color='black')

        average_grade = filtered_df.groupby('Fach')['Note'].mean().round(1).reset_index()

        average_table = dash_table.DataTable(
            columns=[{"name": "Fach", "id": "Fach"},
                     {"name": "Durchschnittsnote", "id": "Note"}],
            data=average_grade.to_dict('records'),
            style_table={'maxHeight': '300px',
                         'overflowY': 'auto',
                         'width': '50%',
                         'margin-left': 'auto',
                         'margin-right': 'auto',
                         'margin-bottom': '30px'},
            style_header={'backgroundColor': 'white', 'color': 'black'},
            style_data={'backgroundColor': 'white', 'color': 'black'}
        )

        return fig, average_table
    else:
        return go.Figure(), html.Div()


if __name__ == '__main__':
    app.run_server(debug=True)