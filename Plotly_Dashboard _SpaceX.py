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
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                html.Div(dcc.Dropdown(id='site-dropdown' ,
                                options=
                                [
                                {'label': 'All Site','value':'All Site'},
                                {'label': 'CCAFS LC-40','value':'CCAFS LC-40'},
                                {'label': 'CCAFS SLC-40','value':'CCAFS SLC-40'},
                                {'label': 'KSC LC-39A','value':'KSC LC-39A'},
                                {'label': 'VAFB SLC-4E','value':'VAFB SLC-4E'}
                                ],
                                #default value
                                value ='All Site', 
                                placeholder='Select a Launch Site here',
                                searchable=True
                                
                                )),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(id='payload-slider' , min = 0 , max=10000, step =1000, marks={

                                    0: '0',
                                    1000 : '1000',
                                    2000: '2000',
                                    3000: '3000',
                                    4000: '4000',
                                    5000: '5000',
                                    6000: '6000',
                                    7000: '7000',
                                    8000: '1000',
                                    9000: '9000',
                                    10000: '1000'
                                }, 
                                value =[min_payload,max_payload] )),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart',component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'))


def generate_chart(get_site_names):
    if get_site_names =='All Site':
        fig = px.pie(spacex_df,names='Launch Site')
        
        return fig

    elif get_site_names == 'CCAFS LC-40':
        df_CCAFS = spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
        fig = px.pie(df_CCAFS ,names='class')
        return fig

    elif get_site_names == 'CCAFS SLC-40':
        df_SLC= spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
        fig = px.pie(df_SLC ,names='class')
        return fig

    elif get_site_names == 'KSC LC-39A':
        df_KSC = spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
        fig = px.pie(df_KSC ,names='class')
        return fig

    elif get_site_names == 'VAFB SLC-4E':
        df_VAFB = spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
        fig = px.pie(df_VAFB,names='class')
        return fig
    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property="value"))

def update_scatter_chart(get_launch_name,get_payload_number):
    
    if get_launch_name =='All Site':
        
        payload_update = spacex_df[(spacex_df['Payload Mass (kg)']>get_payload_number[0]) & (spacex_df['Payload Mass (kg)']<get_payload_number[1])]
        scat = px.scatter(payload_update,x='Payload Mass (kg)' , y='class' , color ="Booster Version Category")
        
        return scat

    elif get_launch_name =='CCAFS LC-40':
        
         df_CCAFS1 = spacex_df[(spacex_df['Launch Site']=='CCAFS LC-40') & (spacex_df['Payload Mass (kg)']>get_payload_number[0]) & (spacex_df['Payload Mass (kg)']<get_payload_number[1])]
         scat = px.scatter(df_CCAFS1,x='Payload Mass (kg)' , y='class' , color ="Booster Version Category")
         
         return scat
         
    elif get_launch_name =='CCAFS SLC-40':
         df_SLC1 = spacex_df[(spacex_df['Launch Site']=='CCAFS SLC-40') & (spacex_df['Payload Mass (kg)']>get_payload_number[0]) & (spacex_df['Payload Mass (kg)']<get_payload_number[1])]
         scat = px.scatter(df_SLC1,x='Payload Mass (kg)' , y='class' , color ="Booster Version Category")
         return scat

    elif get_launch_name =='KSC LC-39A':
         df_KSC1 = spacex_df[(spacex_df['Launch Site']=='KSC LC-39A') & (spacex_df['Payload Mass (kg)']>get_payload_number[0]) & (spacex_df['Payload Mass (kg)']<get_payload_number[1])]
         scat = px.scatter(df_KSC1,x='Payload Mass (kg)' , y='class' , color ="Booster Version Category")
         return scat

    elif get_launch_name =='KSC LC-39A':
         df_VAFB1= spacex_df[(spacex_df['Launch Site']=='KSC LC-39A') & (spacex_df['Payload Mass (kg)']>get_payload_number[0]) & (spacex_df['Payload Mass (kg)']<get_payload_number[1])]
         scat = px.scatter(df_VAFB1,x='Payload Mass (kg)' , y='class' , color ="Booster Version Category")
         return scat
    else:
        scat = px.scatter(spacex_df,x='Payload Mass (kg)' , y='class' , color ="Booster Version Category")
        return scat



    



# Run the app
if __name__ == '__main__':
    app.run_server()