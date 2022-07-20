import dash
from dash.dependencies import Input,Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import PricePredict

app_dash = dash.Dash(__name__,url_base_pathname='/pathname/')

app_dash.layout = html.Div([dcc.Location(id='url',refresh=False),html.Div(id="page")])

@app_dash.callback(Output('page','children'),[Input('url','search')])
def render_template(search):
    df = pd.read_csv(r'C:\Users\aadmohan\Desktop\Howathon\count_send.csv')
    objective = str(df['objective'][0])
    if objective != 'all weather portfolio':
        equity = int(df['equity'][0])
        bond = int(df['bond'][0])
        data = {'Asset Class': ['Equity', 'Bond'], 'percent': [equity, bond]}
        df = pd.DataFrame(data)

        fig = px.pie(df, values='percent', names='Asset Class')

        table_div = table_render()
        body = html.Div([html.H1("Asset Allocation", style={'text-align':'center'}),dcc.Graph(figure=fig),html.H2("Recommended Funds", style={'text-align':'center'}),table_div])

    elif objective == 'all weather portfolio':
        equity = int(df['equity'][0])
        bond = int(df['bond'][0])
        gold = int(df['gold'][0])
        commodity = int(df['commodity'][0])
        data = {'Asset Class': ['Equity', 'Bond','gold','commodity'], 'percent': [equity, bond,gold,commodity]}
        df = pd.DataFrame(data)

        fig = px.pie(df, values='percent', names='Asset Class')

        table_div = table_render(objective)
        body = html.Div([html.H1("Asset Allocation", style={'text-align':'center'}),dcc.Graph(figure=fig),html.H2("Recommended Funds", style={'text-align':'center'}),table_div])

    return body

def table_render(objective):

    #body = html.Table([html.Tr([html.Th("Fund Name"),html.Th("Fund Type"),html.Th("Fund Type")])])
    df = pd.read_csv(r'C:\Users\aadmohan\Desktop\Howathon\table.csv')
    df = df[df['Recommended']=='Y']
    if objective == "all weather portfolio":
        df1 = pd.read_csv(r'C:\Users\aadmohan\Desktop\Howathon\table_all_weather_port.csv')
        df = pd.concat([df,df1])
        df.reset_index(drop=True)

    generate_from_excel_table = html.Div([html.Table([html.Tr([html.Th("Fund Name",style ={'border-collapse': 'collapse','border':'1px solid black'}),html.Th("Fund Type",style ={'border-collapse': 'collapse','border':'1px solid black'}),html.Th("QTD",style ={'border-collapse': 'collapse','border':'1px solid black'}),html.Th("1 year",style ={'border-collapse': 'collapse','border':'1px solid black'}),html.Th("2 year",style ={'border-collapse': 'collapse','border':'1px solid black'}),html.Th("5 year",style ={'border-collapse': 'collapse','border':'1px solid black'}),html.Th('Lifetime',style ={'border-collapse': 'collapse','border':'1px solid black'}),html.Th('Expected Return in 1 yr (%)',style ={'border-collapse': 'collapse','border':'1px solid black'}),html.Th('Recommended',style ={'border-collapse': 'collapse','border':'1px solid black'})], style ={'border-collapse': 'collapse','border':'1px solid black'})] +[html.Tr([html.Td(df.iloc[i][col], style ={'border-collapse': 'collapse','border':'1px solid black','text-align':'center'}) for col in df.columns], style ={'border-collapse': 'collapse','border':'1px solid black'}) for i in range(0,len(df))], style ={'border-collapse': 'collapse','border':'1px solid black','align':'center','margin-left': '230px'})])
    return generate_from_excel_table

if __name__ == '__main__':
    app_dash.run_server(debug=True)