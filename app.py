import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from EU_Option_BSM_GBM_V5 import *
from descriptions import list_input
import base64

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], external_scripts=['https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'])
server = app.server

bg_color="#506784",
font_color="#F3F6FA"

email = "michelvanderhulst@student.uclouvain.be"



graph_rep_strat_text = ''' #### Replication strategy '''

graph_port_details_text = ''' #### Portfolio composition'''
graph_held_shares_text = ''' #### Held shares'''
graph_sde_deriv_text = ''' #### Option greeks '''


def header():
	return html.Div(
                id='app-page-header',
                children=[#html.Div(html.A(
		              #            id='lsm-logo', 
		              #            children=[html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(open("output-onlinepngtools (1).png", 'rb').read()).decode()))],
		              #            href="https://uclouvain.be/en/faculties/lsm",
		              #            target="_blank", #open link in new tab
		              #            style={'margin':'20px'}
		              #              ), style={"display":"inline-block"}),
                    #
                    #
                    # html.Div(
	                   #  html.A(
	                   #  	id="nova-logo", 
	                   #  	children=[html.Img(src="data:image/png;base64,{}".format(base64.b64encode(open("output-onlinepngtools (2).png",'rb').read()).decode()))],
	                   #  	href="https://www2.novasbe.unl.pt/en/",
	                   #  	style={"margin":"-45px"}
	                   #  	  ), style={"display":"inline-block"}),
                    #
                    #
                    html.Div(children=[html.H3("European option replication strategy app"),
                    				   html.H4("Black-Scholes-Merton model")
                    				  ],
                       		 style={"display":"inline-block", "font-family":'sans-serif'}),
                    #
                    #
                    html.Div(children=[dbc.Button("About", id="popover-target", outline=True, style={"color":"white", 'border': 'solid 1px white'}),
                    	      		   dbc.Popover(children=[dbc.PopoverHeader("About"),
                    	      	       		   	             dbc.PopoverBody(["Michel Vanderhulst",                     	    
                    	      	       		   	             				  f"\n {email}", 
                    	      	       		   	             				  html.Hr(), 
                    	      	       		   	             				  "This app was built for my Master's Thesis, under the supervision of Prof. Frédéric Vrins (frederic.vrins@uclouvain.be)."]),],
                    	      	          		   id="popover",
                    	      	          		   is_open=False,
                    	      	          		   target="popover-target"),
                    	      		   ],
                    	      style={"display":"inline-block", "font-family":"sans-serif", 'marginLeft': '60%'}),
                		 ],
                style={
                    'background': bg_color,
                    'color': font_color,
                    'padding':20,
                    'margin':'-10px',
                }
            )



def body():
	return html.Div(children=[
            html.Div(id='left-column', children=[
                dcc.Tabs(
                    id='tabs', value='The app',
                    children=[
                        dcc.Tab(
                            label='The app',
                            value='The app',
                            children=html.Div(children=[
                            	html.Br(),
                                html.H4('What is this app?', style={"text-align":"center"}
                                ),
                                html.P(
                                    """
                                    This app computes the replication strategy of vanilla European options on a set of given input, and compares its value against the traditional Black-Scholes-Merton
                                    price.                           
                                    """
                                ),
                                html.P(
                                    """
                                    The goal is to showcase that the price is truly arbitrage-free, as both the strategy and the Black-Scholes have the same values. 
                                    """
                                ),
                                html.P(
                                    """
                                    Read more about options : 
                                    https://en.wikipedia.org/wiki/Option_(finance)
                                    
                                    """
                                ),
                            ])
                        ),
                        dcc.Tab(
                        	label="Methodology",
                        	value="Methodology",
                        	children=[html.P(children='Will be checked later. Is this \(\pi\) inline with my sentance.'), html.P(children='$$ \lim_{t \\rightarrow \infty} \pi = 0$$')]),
                        		
                        dcc.Tab(
                            label='Input',
                            value='Input',
                            children=html.Div(children=[
                            					html.Br(),
                            					#
                            					html.P(
				                                    """
				                                    Hover your mouse over any input to get its definition.                           
				                                    """
				                                ),
                            					dcc.Dropdown(
                            						id='CallOrPut',
            										options=[{'label':'European Call option', 'value':"Call"},
            		 										 {'label':'European Put option', 'value':"Put"}],
            										value='Call'),
										        #
										        html.Br(),
										        #
										        html.Div(children=[html.Label('Spot price', title=list_input["Spot price"], style={'font-weight': 'bold', "text-align":"center", "width":"25%",'display': 'inline-block'} ),
										            			   dcc.Input(id="S", value=100, type='number', style={"width":"16%", 'display': 'inline-block'}),
										            			   html.Label("Strike", title=list_input["Strike"], style={'font-weight': 'bold',"text-align":"center", "width":"25%",'display': 'inline-block'} ),
										            			   dcc.Input(id="K", value=100, type='number', style={"width":"16%", 'display': 'inline-block'}),
										            			  ],),				       
										    	#
										    	html.Div(children=[html.Label("Drift", title=list_input["Drift"], style={'font-weight': 'bold', 'display': 'inline-block'}),
										    			  		   html.Label(id="drift", style={'display': 'inline-block'}),
										    			  		  ]),
										    	#
										    	dcc.Slider(id='mu', min=-0.30, max=0.30, value=0.10, step=0.01, marks={-0.30: '-30%', 0.30: '30%'}),
										    	#
										    	html.Div([html.Label('Volatility', title=list_input["Volatility"], style={'font-weight': 'bold', "display":"inline-block"}),
										    			  html.Label(id="sigma", style={"display":"inline-block"}),]),  
										    	#
										    	dcc.Slider(id='vol', min=0, max=1, step=0.01, value=0.20, marks={0:"0%", 1:"100%"}),
										        #
										        html.Div([html.Label('Risk-free rate', title=list_input["Risk-free rate"], style={'font-weight': 'bold', "display":"inline-block"}),
										    			  html.Label(id="riskfree", style={"display":"inline-block"}),]),  
										    	dcc.Slider(id='Rf', min=0, max=0.1, step=0.01, value=0.05, marks={0:"0%", 0.1:"10%"}),
										    	#
										    	html.Div([html.Label('Maturity', title=list_input["Maturity"], style={'font-weight':'bold', "display":"inline-block"}),
										    			  html.Label(id="matu", style={"display":"inline-block"}),]),										 
										    	dcc.Slider(id='T', min=0.25, max=5, # marks={i: '{}'.format(i) for i in range(6)},
										    			   marks={0.25:"3 months", 5:"5 years"}, step=0.25, value=3),
										    	#
										    	html.Br(),
										        html.Div([
										            	html.Label('Discretization step', title=list_input["Discretization step"], style={'font-weight': 'bold', "text-align":"left",'width': '50%', 'display': 'inline-block'}),
										            	dcc.Input(id="dt", value=0.01, type='number', style={"width":"16%", 'display': 'inline-block'}),
										        		]),
										        #
										       	html.Div([
										            	html.Label("Portfolio rebalancing", title=list_input["Rebalancing frequency"], style={'font-weight': 'bold', "text-align":"left",'width': '50%', 'display': 'inline-block'}),
										            	dcc.Input(id="dt_p", value=1, type='number', style={"width":"16%", 'display': 'inline-block'}),
										        		]),
										    	#
										    	html.Div([html.Label('Transaction costs', title=list_input["Transaction costs"], style={'font-weight': 'bold', "text-align":"left",'width': '50%', 'display': 'inline-block'}),
										    			  dcc.Input(id="TransactionCosts", value=0, type='number', style={"width":"16%", 'display': 'inline-block'}),
										    			]),
										    	#
										    	dcc.Checklist(
										    		id = "FixedOrPropor",
										       		options=[
										       			{'label': 'Fixed TC', 'value': 'FTC'},
										        		{'label': 'Proportional TC', 'value': 'PTC'}],
										        	value=[], #ADD AN S WHEN GOING ONLINE
										        	labelStyle={'padding':5, 'font-weight': 'bold', "text-align":"left", 'display': 'inline-block'}),
										    	#
										    	dcc.Checklist(
										    		id = "seed",
										       		options=[
										        		{'label': 'Set random generation seed', 'value': "seed"}],
										        	value=[], #ADD AN S WHEN GOING ONLINE
										        	labelStyle={'font-weight': 'bold', "text-align":"left", 'display': 'inline-block'}
										        	),
                                            	])),],),
        ], style={'float': 'left', 'width': '25%', 'margin':"30px"}),
	])


def graphs():
	return html.Div(id='right-column', 
					children=[
						html.Br(),
						html.Div([
				        	html.Div(children=[dcc.Markdown(children=graph_port_details_text),
					        				   dcc.Graph(id='port_details'),],
					        		 style={"float":"right", "width":"45%", "display":"inline-block"}),
				        	html.Div(children=[dcc.Markdown(children=graph_rep_strat_text),
				        					  dcc.Graph(id='replication'),],
				        			 style={"float":"right", "width":"55%", "display":"inline-block"}),
				        		]),
			        	html.Div([
			        		html.Div(children=[dcc.Markdown(children=graph_sde_deriv_text),
				        					   dcc.Graph(id='sde_deriv'),],
				        			 style={"float":"right", "width":"45%", "display":"inline-block"}),
			        		html.Div(children=[dcc.Markdown(children=graph_held_shares_text),
			        						   dcc.Graph(id='held_shares'),],
			        				 style={"float":"right", "width":"55%", "display":"inline-block"}),
				        		]),
							 ], 
					style={'float': 'right', 'width': '70%'})


app.layout = html.Div(
				id='main_page',
        		children=[
            		dcc.Store(id='memory-output'),
            		header(),
            		body(),
            		graphs(),
        		 		 ],
    				 )


@app.callback(
	Output('memory-output', 'data'),
	[Input('CallOrPut', 'value'),
     Input("S","value"),
     Input("K", "value"),
     Input("Rf", "value"),
     Input("T","value"),
     Input("mu","value"),
     Input("vol", "value"),
     Input("dt", "value"),
     Input("dt_p", "value"),
     Input("TransactionCosts", "value"),
	 Input("FixedOrPropor", "value"),
     Input("seed", "value"),])
def get_rep_strat_data(CallOrPut, S, K, Rf,T,mu,vol,dt,dt_p, TransactionCosts, FixedOrPropor, sde__seed):
	dt, K, discre_matu, StockPrice, OptionIntrinsicValue, OptionPrice, EquityAccount, CashAccount, Portfolio, V_t, f_t, f_x, f_xx = RepStrat_EU_Option_BSM_GBM_V5(CallOrPut, S, K, Rf, T, mu, vol, dt, dt_p, TransactionCosts, FixedOrPropor,  sde__seed)			
	return dt, K, list(discre_matu), StockPrice, OptionIntrinsicValue, OptionPrice, EquityAccount, CashAccount, Portfolio, V_t, f_t, f_x, f_xx


@app.callback(
    Output('replication', 'figure'),
    [Input('memory-output', 'data'),])
def graph_rep_strat(data):
	dt, K, discre_matu, StockPrice, OptionIntrinsicValue, OptionPrice, EquityAccount, CashAccount, Portfolio, V_t, f_t, f_x, f_xx = data

	return{
    'data': [
        go.Scatter(
            x=discre_matu,
            y=StockPrice,
            mode='lines',
            opacity=0.7,
            name="Stock price simulation (GBM)"),
        # go.Scatter(
        # 	x=discre_matu,
        # 	y=[K]*len(discre_matu),
        # 	mode='lines',
        # 	opacity=0.7,
        # 	name=f"Strike = {K}",
        # 	),
        go.Scatter(
        	x=discre_matu,
        	y=OptionIntrinsicValue,
        	mode="lines",
        	opacity=0.7,
        	name="Option intrinsic value"),
        go.Scatter(
        	x=discre_matu,
        	y=OptionPrice,
        	mode="lines",
        	opacity=0.7,
        	name="Option price"),
        go.Scatter(
        	x=discre_matu,
        	y=V_t,
        	mode="lines",
        	opacity=0.7,
        	name="SDE simulation"),  
        go.Scatter(
        	x=discre_matu,
        	y=Portfolio,
        	mode="lines",
        	opacity=0.7,
        	name="Portfolio"),
        go.Scatter(
        	x=[None], 
        	y=[None], 
        	mode='markers',
            name=f'Payoff - Portfolio: {round(OptionIntrinsicValue[-1]-EquityAccount[-1]-CashAccount[-1],2)}'),
    ],
    'layout': go.Layout(
        title={'yref':"paper",
        		'y':1,
        		"yanchor":"bottom"},
        margin={"t":15},
        xaxis={'title': f"Discretized time to maturity"},
        yaxis={'title': "Currency"},
        legend=dict(
	        x=0,
	        y=1,
	        traceorder='normal',
	        bgcolor='rgba(0,0,0,0)'),
    )
}


@app.callback(
    Output('port_details', 'figure'),
    [Input('memory-output', 'data'),])
def graph_portf_details(data):
	dt, K, discre_matu, StockPrice, OptionIntrinsicValue, OptionPrice, EquityAccount, CashAccount, Portfolio, V_t, f_t, f_x, f_xx = data
	return{
    'data': [
        go.Scatter(
            x=discre_matu,
            y=EquityAccount,
            mode='lines',
            opacity=0.7,
            name="Equity account"),
        go.Scatter(
        	x=discre_matu,
        	y=CashAccount,
        	mode='lines',
        	opacity=0.7,
        	name="Cash account",
        	),
        go.Scatter(
        	x=discre_matu,
        	y=Portfolio,
        	mode="lines",
        	opacity=0.7,
        	name="Portfolio"),
    ],
    'layout': go.Layout(
        margin={"t":15},
        xaxis={'title': f"Discretized time to maturity"},
        yaxis={'title': "Currency"},
        legend=dict(
	        x=0,
	        y=1,
	        traceorder='normal',
	        bgcolor='rgba(0,0,0,0)'),
    )
}

@app.callback(
    Output('held_shares', 'figure'),
    [Input('memory-output', 'data'),])
def graph_portf_details(data):
	dt, K, discre_matu, StockPrice, OptionIntrinsicValue, OptionPrice, EquityAccount, CashAccount, Portfolio, V_t, f_t, f_x, f_xx = data
	return{
    'data': [
        go.Scatter(
        	x=discre_matu,
        	y=f_x,
        	mode='lines',
        	opacity=0.7,
        	name="Held shares",
        	),
    ],
    'layout': go.Layout(
        margin={"t":15},
        xaxis={'title': f"Discretized time to maturity"},
        yaxis={'title': "Currency"},
        legend=dict(
	        x=0,
	        y=1,
	        traceorder='normal',
	        bgcolor='rgba(0,0,0,0)'),
    )
}

@app.callback(
    Output('sde_deriv', 'figure'),
    [Input('memory-output', 'data'),])
def graph_portf_details(data):
	dt, K, discre_matu, StockPrice, OptionIntrinsicValue, OptionPrice, EquityAccount, CashAccount, Portfolio, V_t, f_t, f_x, f_xx = data
	return{
    'data': [
        go.Scatter(
            x=discre_matu,
            y=f_t,
            mode='lines',
            opacity=0.7,
            name="Theta"),
        go.Scatter(
        	x=discre_matu,
        	y=f_x,
        	mode='lines',
        	opacity=0.7,
        	name="Delta",
        	),
        go.Scatter(
        	x=discre_matu,
        	y=f_xx,
        	mode="lines",
        	opacity=0.7,
        	name="Gamma"),
    ],
    'layout': go.Layout(
        #height=400,
        margin={"t":15},
        xaxis={'title': f"Discretized time to maturity"},
        yaxis={'title': "Currency"},
        legend=dict(
	        x=0,
	        y=1,
	        traceorder='normal',
	        bgcolor='rgba(0,0,0,0)'),
    )
}


@app.callback(Output('drift', 'children'),
              [Input('mu', 'value')])
def display_value(value):
    return f': {int(value*100)}%'

@app.callback(Output('sigma', 'children'),
			  [Input('vol', 'value')])
def display_value2(value):
    return f': {int(value*100)}%'

@app.callback(Output('riskfree', 'children'),
			  [Input('Rf', 'value')])
def display_value3(value):
    return f': {int(value*100)}%'

@app.callback(Output('matu', 'children'),
			  [Input('T', 'value')])
def display_value4(value):
	if value==0.25 or value==0.5 or value==0.75:
		return f": {int(value*12)} months"
	elif value == 1:
		return f': {value} year'
	else:
		return f': {value} years'

@app.callback(
    Output("popover", "is_open"),
    [Input("popover-target", "n_clicks")],
    [State("popover", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open




if __name__ == '__main__':
    app.run_server(debug=True)