from flask import Flask, session, Request, redirect, Response, jsonify   
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from keycloak.extensions.flask import AuthenticationMiddleware
import requests 
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

server= Flask(__name__)
app = Dash(__name__, server=server, url_base_pathname="/home/")
server = app.server
server.config["SECRET_KEY"] = "Z5sJpXp6d7bB1LFHws0FDcQyxTyG0vnF"
server.wsgi_app = AuthenticationMiddleware(
    server.wsgi_app,
    server.config,
    server.session_interface,
    callback_url="http://127.0.0.1:5001/test/",
    login_redirect_uri="/back",
    logout_uri = "/logout", # Configure Keycloak 
    logout_redirect_uri="/logout2",
)
#
@server.route('/logout2')
def logout():
    return "User logged out successfully"
import json
@server.route('/back')
def root_path():
    #token = json.loads(session['tokens'])['access_token']
    #headers={'Authorization': f'Bearer {token}'}
    #par = {"access_token": f"{token}"}
    #r = requests.get(f"http://127.0.0.1:8081/__health")
    #r = requests.get("http://127.0.0.1:8081/keycloak-protected", headers=headers, allow_redirects=True)
    
    return 'OK'


# app.layout = html.Div([
#     html.H6("Change the value in the text box to see callbacks in action!"),
#     html.Div([
#         "Input: ",
#         dcc.Input(id='my-input', value='initial value', type='text')
#     ]),
#     html.Br(),
#     html.Div(id='my-output'),

# ])

# import json
# @callback(
#     Output(component_id='my-output', component_property='children'),
#     Input(component_id='my-input', component_property='value')
# )
# def update_output_div(input_value):
#     #kc =json.loads(session['user'])['sub']
#     token = json.loads(session['tokens'])['access_token']
#     headers={'Authorization': f'Bearer {token}'}
#     #par = {"access_token": f"{token}"}
#     #r = requests.get(f"http://127.0.0.1:5001/backend",headers=headers)
#     r = requests.get("http://127.0.0.1:5001/backend", allow_redirects=True)
#     return f'Output:{r.raw}'

if __name__ == '__main__':
	server.run_server(debug=True)