# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                  options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                    ],
                                  value= 'ALL',
                                  placeholder='Select a Launch Site here',
                                  searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min = 0,
                                    max = 10000,
                                    step = 1000,
                                    marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                    value = [0, 1000]
                                    ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown',component_property='value'))

def display_pie_chart(selected_site):
    if selected_site == 'ALL':
        sites_successful_launches = spacex_df.groupby('Launch Site')['class'].count().reset_index()
        fig = px.pie(data_frame=sites_successful_launches, values='class', 
        names='Launch Site', 
        title='Total Successful Launches by Site')
        return fig
    else:
        site_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        site_launches = site_df.groupby('class')['Flight Number'].count().reset_index()
        fig = px.pie(data_frame=site_launches, values='Flight Number', 
        names='class', 
        title=f'Total Successful Launches for Site {selected_site}')
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])

def display_scatter_chart(selected_site, selected_payload):
    if selected_site == 'ALL':
        payload_df= spacex_df[(spacex_df['Payload Mass (kg)'] >= selected_payload[0])&(spacex_df['Payload Mass (kg)'] <= selected_payload[1])]
        fig = px.scatter(data_frame=payload_df, x='Payload Mass (kg)', 
        y='class', color='Booster Version Category',
        title='Correlation between Payload and Success for All Sites')
        return fig
    else:
        site_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        payload_df= site_df[(site_df['Payload Mass (kg)'] >= selected_payload[0])&(site_df['Payload Mass (kg)'] <= selected_payload[1])]
        fig = px.scatter(data_frame=payload_df, x='Payload Mass (kg)', 
        y='class', color='Booster Version Category',
        title=f'Correlation between Payload and Success for Site {selected_site}')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
