import pandas as pd
import dash
from dash import html,dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt

app = dash.Dash(__name__)

app.config.suppress_callback_exceptions = True

df = pd.read_csv('Historical_Wildfires.csv')
df['Month'] = pd.to_datetime(df['Date']).dt.month_name()
df['Year'] = pd.to_datetime(df['Date']).dt.year

app.layout = html.Div(children=[html.H1('Austrailian Wildfire Dasboard', style={'textAlign':'centre','color': '#503D36','font-size':26}),
                        html.Div([
                            html.H2('Select Region', style={'margin-right':'2em'}),

                            dcc.RadioItems(df.Region.unique(),'NSW',id='region',inline=True),
                                           
                        html.Div([
                            html.H2('Select Year',style={'margin-right':'2em'}),
                            dcc.Dropdown(df['Year'].unique(), value=2005, id='year')
                                ]),
                        html.Div([
                            html.Div([ ], id='plot1'),
                            html.Div([ ],id='plot2')
                        ])
                        ])        
                        ])

@app.callback([Output(component_id='plot1',component_property='children'),
               Output(component_id='plot2', component_property='children')],
                [Input(component_id='region', component_property='value'),
                 Input(component_id='year', component_property='value' )])


def reg_year_display(input_region,input_year):
    region_data = df[df['Region'] == input_region]
    yr_data = region_data[region_data['Year'] == input_year]
    est_data = yr_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1= px.pie(est_data,names='Month',values='Estimated_fire_area',title='{}: Monthly Average Estimated Fire Area in year{}'.format(input_region,input_year))

    veg_data = yr_data.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(veg_data,x='Month',y='Count',title='{}: Average Count of Pixels for presumed Vegetation Fire in Year {}'.format(input_region,input_year))

    return [dcc.Graph(figure=fig1)
            ,dcc.Graph(figure=fig2)]

if __name__ == '__main__':
    app.run()