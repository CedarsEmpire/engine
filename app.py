import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Shareholder Dashboard'),
    html.Div([
        html.H2('Investment Overview'),
        html.P('Display shareholder\'s investment details')
    ]),
    html.Div([
        html.H2('Balance and Earnings'),
        html.P('Show shareholder\'s balance and earnings')
    ]),
    html.Div([
        html.H2('Transaction History'),
        html.P('Display shareholder\'s transaction history')
    ]),
    html.Div([
        html.H2('Deposit'),
        html.P('Allow shareholders to deposit funds into their accounts')
    ]),
    html.Div([
        html.H2('Referral'),
        html.P('Implement a referral system where shareholders can refer others and earn rewards')
    ]),
    html.Div([
        html.H2('Live Chat'),
        html.P('Integrate a live chat feature that enables shareholders to communicate with Cedars customer support')
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
