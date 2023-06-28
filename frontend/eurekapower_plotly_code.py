# SOPPCO project 
from flask import Flask
import dash
#import dash_core_components as dcc
from dash import dcc
from dash import html
#import dash_html_components as html
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
#import dash_table 
from dash import dash_table
from dash.dependencies import Input, Output
import requests
import json
from datetime import datetime
from flask import session
from keycloak.extensions.flask import AuthenticationMiddleware

# user = json.loads(session["user"])
# user["sub"]

# xxx= 0
# # url_keycloak = 'http://127.0.0.1:5000/users/contract-id'
# # resp = requests.get(url=url_keycloak+'/'+str(xxx))
# # resp_data = resp.json()
# # _contract_account_id=resp_data['contract_account_id']
#_contract_account_id = 363000024

def api_account(_contract_account_id):
    headers = {"Content-Type": "application/json"}

    url_account_details = 'http://127.0.0.1:5000/users/userinfo'
    r = {'contract_account_id': _contract_account_id}
    data = json.dumps(r)
    resp = requests.post(url=url_account_details, data=data, headers=headers)
    resp_data = resp.json()
    acc_details_list = resp_data['AR_PAROXIS_11,Square_Meters,PoD_Postal_Code']
    acc_details=acc_details_list[0]
    ar_paroxis=acc_details[0]
    sq_meters=acc_details[1]
    code=acc_details[2]
    dict_account_details={'account details':['customer number','postal code','area (sq. meters)'],
            'personal info':[ar_paroxis,code,sq_meters]}
    df_account=pd.DataFrame(dict_account_details)
    return df_account
    
def api_prediction(_contract_account_id):

    headers = {"Content-Type": "application/json"}
    url_prediction = 'http://127.0.0.1:5000/predict/consumption'
    r = {'contract_account_id': _contract_account_id}
    data = json.dumps(r)
    resp = requests.post(url=url_prediction, data=data, headers=headers)
    resp_data = resp.json()
    prediction = resp_data['prediction']
    currentMonth = datetime.now().month
    currentYear=datetime.now().year
    monthyear=[]
    for i in range(1,13):
        if currentMonth+i>12:
            next_month=currentMonth+i-12
            next_year=currentYear+1
        else:
            next_month=currentMonth+i
            next_year=currentYear
        monthyear.append(str(next_month)+'/'+str(next_year))
    
    dict_prediction={'Month':monthyear,'consumption':prediction}
    df_future = pd.DataFrame(dict_prediction)

    # Create a line chart for monthly energy consumption prediction
    fig1 = px.line(df_future, x="Month", y="consumption", title="Monthly Energy Consumption prediction")

    return fig1
    

def api_history(_contract_account_id):
    headers = {"Content-Type": "application/json"}

    url_account_details = 'http://127.0.0.1:5000/users/historical_data'
    r = {'contract_account_id': _contract_account_id}
    data = json.dumps(r)
    resp = requests.post(url=url_account_details, data=data, headers=headers)
    resp_data = resp.json()

    Year=[]
    Month=[]
    Total_Consumption=[]
    Metering_Period=[]
    PoD_Postal_Code=[]
    Square_Meters=[]
    raw_data_list = resp_data['Year,Month,Total_Consumption,Metering_Period,PoD_Postal_Code,Square_Meters']
    db_postal_code=None
    for element in raw_data_list:
        Year.append(element[0])
        Month.append(element[1])
        Total_Consumption.append(element[2])
        Metering_Period.append(element[3])
        PoD_Postal_Code.append(element[4])
        db_postal_code=element[4]
        Square_Meters.append(element[5])
    dict_raw_data={'Year':Year,
                'Month':Month,
                'Total_Consumption':Total_Consumption,
                'Metering_Period':Metering_Period,
                'PoD_Postal_Code':PoD_Postal_Code,
                'Square_Meters':Square_Meters}

    columns_needed = ['Year', 'Month', 'Total_Consumption', 'Metering_Period', 'PoD_Postal_Code', 'Square_Meters']

    df_PPC_SOPPCO = process_consumption_data(dict_raw_data, columns_needed)
    #df_PPC_SOPPCO.info()
    postal_code_input=db_postal_code

    return df_PPC_SOPPCO, postal_code_input
########### FUNCTION THAT PROCESSES DATA - PAPALOUKAS ####################################################################################3
def process_consumption_data(dictt, columns_needed):
     # Read data
     df = pd.DataFrame(dictt)
     # get_yearly_consumption(id, year)   ********************************* Rest APIs ******************************************

     # create dataframe with the columns I'm interested in 
     df = df.loc[:, ['Year', 'Month', 'Total_Consumption', 'Metering_Period', 'PoD_Postal_Code', 'Square_Meters']]

     # create for each series marked Bimothly a new one with half consumption and marked Monthly
     bimonthly_rows = df[df['Metering_Period'] == 'Bimonthly']

     modified_rows = pd.DataFrame({
     'Metering_Period': 'Monthly',
     'Total_Consumption': bimonthly_rows['Total_Consumption'] / 2,
     # Copy over the other columns from the bimonthly rows
     'Year': bimonthly_rows['Year'],
     'Month': bimonthly_rows['Month'],
     'PoD_Postal_Code': bimonthly_rows['PoD_Postal_Code'],
     'Square_Meters': bimonthly_rows['Square_Meters'],
     })

     df = pd.concat([df, modified_rows], ignore_index=True)

     # convert the Bimonthly series to monthly with half consumption 
     # Identify rows where Metering_Period is "Bimonthly"
     bimonthly_rows = df[df['Metering_Period'] == 'Bimonthly']

     # Change Metering_Period to "Monthly", divide Total_Consumption by 2 and suitable month
     df.loc[bimonthly_rows.index, 'Metering_Period'] = 'Monthly'
     df.loc[bimonthly_rows.index, 'Total_Consumption'] /= 2
     df.loc[bimonthly_rows.index, 'Month'] -=1

     #sort table first by PoD_Postal_Code column then by Year and finally by Month column
     df = df.sort_values(by=['PoD_Postal_Code', 'Year', 'Month'])

     # counter for negative consumptions 
     num_negativesconsumptions = df[df['Total_Consumption'] < 0]['Total_Consumption'].count()

     #replace negative with Nan
     df.loc[df['Total_Consumption'] < 0, 'Total_Consumption'] = np.nan

     # delete rows with Nan consumption 
     df.dropna(subset=['Total_Consumption'], inplace=True)

     return df
########################################## ENDS FUNCTION THAT PROCESSES DATA - PAPALOUKAS ####################################################



# Create a Dash app #############################################################################################################
#app = dash.Dash(__name__)   
server= Flask(__name__)
app = dash.Dash(__name__, server=server, url_base_pathname="/home/")
server = app.server
server.config["SECRET_KEY"] = "Z5sJpXp6d7bB1LFHws0FDcQyxTyG0vnF"
server.wsgi_app = AuthenticationMiddleware(
    server.wsgi_app,
    server.config,
    server.session_interface,
    callback_url="http://127.0.0.1:5001/test/",
    login_redirect_uri="/home/",
    logout_uri = "/logout", # Configure Keycloak 
    logout_redirect_uri="/home",
)

app.layout = html.Div(
    #background photo parameters 
    style={
    'background-color': '#f2f2f2',  # Background color
    'background-image': 'url("assets/clean_energy.jpg")',  # Background image
    'background-size': 'cover',  # Adjust background image size
    'background-position': 'center',  # Adjust background image position
    'height': '100vh',  # Set the height of the layout to occupy the entire viewport height
    'padding': '50px'  # Add padding to the content within the layout
    },
    children=[
    dcc.Tabs(id='tabs', value='tab-1', children=[
        dcc.Tab(label='Personal Information', value='Personal Information', style={'font-family': 'Georgia', 'font-size': '20px'}),
        dcc.Tab(label='Historical data for energy consumption', value='Historical data for energy consumption', style={'font-family': 'Georgia', 'font-size': '20px'}),
        dcc.Tab(label='Prediction for energy consumption', value='Prediction for energy consumption', style={'font-family': 'Georgia', 'font-size': '20px'}),
        dcc.Tab(label='Gamification', value='Gamification', style={'font-family': 'Georgia', 'font-size': '20px'})
    ]),
    html.Button(id="logout-button", children="Logout", style={'position': 'absolute', 'top': '10px', 'right': '10px'}),
        html.Div(id="logout-message"),
    html.Div(id='content')
])

# @app.callback(
#     dash.dependencies.Output("logout-message", "children"),
#     [dash.dependencies.Input("logout-button", "n_clicks")]
# )
# def logout(n_clicks):
#     if n_clicks is not None and n_clicks > 0:
#         r = requests.get("http://127.0.0.1:5001/logout", allow_redirects=True)
#         # Perform logout operations here, e.g., clear session or user authentication state
#         return r.url()
#     else:
#         pass

@app.callback(Output('content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    user = json.loads(session["user"])
    xxx= user["sub"]
    url_keycloak = 'http://127.0.0.1:5000/users/contract-id'
    resp = requests.get(url=url_keycloak+'/'+str(xxx))
    resp_data = resp.json()
    _contract_account_id=resp_data['contract_account_id']
    
    if tab == 'Personal Information':
        df_account = api_account(_contract_account_id)
        return html.Div([
            html.H1('Welcome to EurekaPower app!', style={'backgroundColor': '#FF5733', 'padding': '10px', 'textAlign': 'center', 'margin-bottom': '100px', }),
            html.H2('Here are your Personal information:'), 
           dash_table.DataTable(
                id='account-details',
                columns=[{"name": i, "id": i} for i in df_account.columns],
                data=df_account.to_dict('records'),
                style_data={
                    'font-family': 'Georgia',
                    'font-size': '25px', 
                    'backgroundColor': 'transparent'
                }, 
                style_table={
                'height': '400px',  # Specify the desired height for the table
                'width': '600px',   # Specify the desired width for the table
                'overflowY': 'auto', # Enable vertical scrolling if necessary
                'font-family': 'Georgia',
                'font-size': '25px', 
                'backgroundColor': 'transparent'
                },
                style_cell={
                    'height': 'auto',   # Allow the row height to adjust to the content
                    'whiteSpace': 'normal'  # Allow cell content to wrap if necessary
                }
            ),
            html.Div(
            style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'},
            children=[
                html.Img(src='assets/dei.svg', alt='image', style={'width': '400px', 'height': 'auto'})
            ]
        ),
        ])
    elif tab == 'Historical data for energy consumption':
        _, postal_code_input = api_history(_contract_account_id)
        return html.Div([
            html.H1("Monthly Energy Consumption", style={'backgroundColor': '#ADD8E6', 'padding': '10px', 'textAlign': 'center', 'margin-bottom': '100px', }),
            #html.Label("Enter a zipcode:"),
            #dcc.Input(id="postal-code-input", type="number", value=55132), edo to allaxa na to pernei xerato ...tha thelei allagi me vasi json ti tou dino
            dcc.Input(id="postal-code-input", type="number", value=postal_code_input, disabled=False),
            dcc.Graph(id="energy-consumption", 
                    figure={'layout':{
                        'xaxis': {'showgrid': False, 'tickfont': {'size': 14}},
                        'yaxis': {'showgrid': False}
                         }          
                    }),
            #check how to make gridlines transparent 
            # to present peak and min value 
            # html.H3('Peak and Minimum Values'),
            #    html.Table(
            #        children=[
            #           html.Tr(children=[
            #                html.Td('Peak Value:'),
            #                html.Td(peak_value)
            #            ]),
            #            html.Tr(children=[
            #                html.Td('Minimum Value:'),
            #                html.Td(min_value),])]), 
            html.Br(),
            html.Div(
            style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'},
            children=[
                html.Img(src='assets/dei.svg', alt='image', style={'width': '400px', 'height': 'auto'})
            ])
        ]),  
        
    elif tab == 'Prediction for energy consumption':
        fig1 = api_prediction(_contract_account_id)
        return html.Div([
            html.H1("Energy Consumption prediction", style={'backgroundColor': '#ADD8E6', 'padding': '10px', 'textAlign': 'center', 'margin-bottom': '100px', }), 
            dcc.Graph(id="energy-prediction", figure=fig1 ),
            html.Br(),
            #show message with the average consumption and take this parameter to ...
            #show message with peak and min value 
            #show comparison to last year 
            html.Div(
            style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'},
            children=[
            html.Img(src='assets/dei.svg', alt='image', style={'width': '400px', 'height': 'auto'})]
        )
        ]),   
    elif tab == 'Gamification':
        
        return html.Div(
        style={'margin': '100px', 'justifyContent': 'center', 'alignItems': 'center', 'textAlign': 'center', },
        children=[
        html.H1("Let's play a game! Tell us the percentage of energy savings and find out your discount! ",
                style={'backgroundColor': '#FF5733', 'padding': '10px', 'textAlign': 'center', 'margin-bottom': '50px', }),
        dcc.Slider(
            id="energy-savings-slider",
            min=0,
            max=100,
            step=5,
            value=10,
            marks={10: "10%", 20: "20%", 30: "30%", 40: "40%", 50: "50%", 60: "60%", 70: "70%", 80: "80%", 90: "90%", 100: "100%"},

        ),
        html.Div(id="energy-savings-message", style={'margin-bottom': '100px', 'margin-top': '50px', 'font-size': '50px'}),
        html.Div(
            style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'},
            children=[
                html.Img(src='assets/dei.svg', alt='image', style={'width': '400px', 'height': 'auto'})
            ]
        ),
    ]
)
############## Define the callback function to update the graph for consumption ##############################################################################
@app.callback(
    dash.dependencies.Output("energy-consumption", "figure"),
    [dash.dependencies.Input("postal-code-input", "value")]
)
def update_figure(postal_code):
    user = json.loads(session["user"])
    xxx= user["sub"]
    url_keycloak = 'http://127.0.0.1:5000/users/contract-id'
    resp = requests.get(url=url_keycloak+'/'+str(xxx))
    resp_data = resp.json()
    _contract_account_id=resp_data['contract_account_id']
    df_PPC_SOPPCO, _ = api_history(_contract_account_id)
    filtered_df = df_PPC_SOPPCO[df_PPC_SOPPCO["PoD_Postal_Code"] == postal_code]
    #peak_value=np.max(df_PPC_SOPPCO[df_PPC_SOPPCO["Total_Consumption"]])
    #min_value= np.min(df_PPC_SOPPCO[df_PPC_SOPPCO["Total_Consumption"]])
    fig = px.line(filtered_df, x="Month", y="Total_Consumption",color="Year", title="Monthly Energy Consumption")
    return fig
##############################################################################################################################################################

# Define the callback function to update the energy savings message - GAMIFICATION ###########################################################################
@app.callback(
    dash.dependencies.Output("energy-savings-message", "children"),
    [dash.dependencies.Input("energy-savings-slider", "value")]
)
def update_energy_savings_message(value):
    if  value < 20:
        message = "You should have a bigger reduction in your energy consumption to get a discount"
    elif value == 20:
        message = "You have an additional 20% discount"
    elif value == 30:
        message = "Good work! You have an additional 30% discount"
    elif value == 50:
        message = "Well done! You have an additional 50% discount"
    elif value >60:
        message = "Wow! You succeeded a significant reduction in energy consumption. Contact your energy provider directly to get you reward!"
    return message


if __name__ == '__main__':
    app.run_server(debug=True)