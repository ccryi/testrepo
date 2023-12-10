import pandas as pd
import dash
from dash import html as html
from dash import dcc as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout

unique_sites = spacex_df['Launch Site'].unique().tolist()
unique_sites.insert(0,'All Sites')


app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                   id='site-dropdown',
                                   options=[
                                    {'label': i, 'value': i} for i in unique_sites],
                                    placeholder="Select a Launch Site here",
                                    value='All Sites',
                                    searchable=True),
                            
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0,
                                max=10000,
                                step=1000,
                                value=[min_payload,max_payload],
                                marks={
                                0: '0 kg',
                                2500: '2500',
                                5000: '5000',
                                7500: '7500',
                                10000: '10000'
                                }),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
Output(component_id='success-pie-chart', component_property='figure'),
Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):	
    filtered_df = spacex_df	
    if entered_site == 'All Sites':	
        fig = px.pie(filtered_df, values='class',	
        labels= {'class':'Total'},	
        names='Launch Site', 	
        title='Total Successes for All Launch Sites')	
       	
    else:	
        filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site]["class"].value_counts().to_frame()	
        filtered_df["name"] = ["Failure", "Success"]	
        fig = px.pie(filtered_df, values='class', names='name', title='Total Success Launches for ' + entered_site)	
    return fig	



# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
Output(component_id='success-payload-scatter-chart', component_property='figure'),
[Input(component_id='site-dropdown', component_property='value'),
Input(component_id='payload-slider', component_property='value')]
)

def get_scatter_chart(entered_site, payload):
    print(entered_site)
    print(payload)
    if entered_site == 'All Sites':
        new_df = spacex_df
        new_df2 = new_df[new_df["Payload Mass (kg)"]>=payload[0]]
        new_df3 = new_df2[new_df["Payload Mass (kg)"]<=payload[1]]
        fig2 = px.scatter(new_df3, y="class", x="Payload Mass (kg)", 
        color= "Booster Version Category", 
        title="Correlation between Payload Mass (Kg) and Launch Outcome")
    else:
        new_df = spacex_df[spacex_df["Launch Site"]==entered_site]
        new_df2 = new_df[new_df["Payload Mass (kg)"]>=payload[0]]
        new_df3 = new_df2[new_df["Payload Mass (kg)"]<=payload[1]]
        fig2 = px.scatter(new_df3, y="class", x="Payload Mass (kg)", 
        color="Booster Version Category", 
        title="Correlation between Payload Mass (Kg) and Launch Outcome")
    return fig2   
# Run the app
if __name__ == '__main__':
    app.run_server()  
