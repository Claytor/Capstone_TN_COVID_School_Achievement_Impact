#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import dash
from dash import Dash, Input, Output, dcc, html
from jupyter_dash import JupyterDash

# Load Data
assessments = pd.read_pickle('../data/school_based/assessments_clean.pkl')

# Get the available levels, student groups, and subject areas
available_levels = assessments['school_lvl'].unique()
available_groups = assessments['student_group'].unique().tolist()

# Define CSS Stylesheet
external_stylesheets = [dbc.themes.LUX]

# Define app with external scripts and stylesheets
app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = html.Div([
    html.H1("Achievement Testing Group Comparisons", style={'text-align': 'center'}),
    dbc.Row([
        dbc.Col([
            html.H2("Proficiency by School Level"),
            dcc.Dropdown(
                id='school-level-dropdown',
                options=[{'label': level, 'value': level} for level in available_levels],
                value=available_levels[0],
                clearable=False,
            ),
            dcc.Graph(id='all-students-graph')
        ], width=6),
        dbc.Col([
            html.H2("Proficiency By Student Group"),
            dcc.Dropdown(
                id='student-group-dropdown',
                options=[{'label': group, 'value': group} for group in available_groups],
                value=available_groups[1],
                clearable=False,
            ),
            dcc.Graph(id='selected-group-graph')
        ], width=6)
    ]),
])

# Define callback to update the "All Students" graph
@app.callback(
    Output('all-students-graph', 'figure'),
    [Input('school-level-dropdown', 'value')]
)
def update_all_students_graph(level):
    # Filter DataFrame based on selected level and "All Students" group
    filtered_data = assessments[(assessments['school_lvl'] == level) & (assessments['student_group'] == 'All Students')]

    # Calculate average values for each year and subject area
    average_data = filtered_data.groupby(['year', 'subject_area'])['pct_met_exceeded'].mean().reset_index()

    # Convert average values from decimal form to percentage form
    average_data['pct_met_exceeded'] = average_data['pct_met_exceeded'] * 100

    # Create a line chart for "All Students"
    fig = px.line(
        average_data,
        x='year',
        y='pct_met_exceeded',
        color='subject_area',
        title=f'{level} School: Average Proficiency Scores (All Students)',
        labels={'year': 'Year', 'pct_met_exceeded': 'Average Proficiency Score (%)'},
    )

    # Update layout
    fig.update_layout(
        legend_title='Subject Area',
        yaxis_title='Average Proficiency Score (%)',
        xaxis=dict(type='category'),  # Set x-axis type to 'category'
        yaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=10,
            range=[0, 100]
        )
    )

    # Add data points as dots
    fig.update_traces(mode='markers+lines', marker=dict(size=5))

    return fig

# Define callback to update the selected student group graph
@app.callback(
    Output('selected-group-graph', 'figure'),
    [Input('school-level-dropdown', 'value'),
     Input('student-group-dropdown', 'value')]
)
def update_selected_group_graph(level, group):
    # Filter DataFrame based on selected level and student group
    filtered_data = assessments[(assessments['school_lvl'] == level) & (assessments['student_group'] == group)]

    # Calculate average values for each year and subject area
    average_data = filtered_data.groupby(['year', 'subject_area'])['pct_met_exceeded'].mean().reset_index()

    # Convert average values from decimal form to percentage form
    average_data['pct_met_exceeded'] = average_data['pct_met_exceeded'] * 100

    # Create a line chart for the selected student group
    fig = px.line(
        average_data,
        x='year',
        y='pct_met_exceeded',
        color='subject_area',
        title=f'{level} School: Average Proficiency Scores ({group})',
        labels={'year': 'Year', 'pct_met_exceeded': 'Average Proficiency Score (%)'},
    )

    # Update layout
    fig.update_layout(
        legend_title='Subject Area',
        yaxis_title='Average Proficiency Score (%)',
        xaxis=dict(type='category'),  # Set x-axis type to 'category'
        yaxis=dict(
            tickmode='linear',
            tick0=0,
            dtick=10,
            range=[0, 100]
        )
    )

    # Add data points as dots
    fig.update_traces(mode='markers+lines', marker=dict(size=5))

    return fig

# Run the app in Jupyter Notebook mode
app.run_server(mode='inline')

