import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load dataset
URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv'
df = pd.read_csv(URL)

# 4.1: Initialize Dash Application
app = dash.Dash(__name__)
app.title = "Automobile Sales Statistics Dashboard"

year_list = [i for i in range(1980, 2024, 1)]

# 4.2 & 4.3: Layout with Dropdowns and Output Division
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
    
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            placeholder="Select a report type",
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
        )
    ]),
    
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder="Select Year",
            style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
        )
    ]),
    
    # 4.3: Output division
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flex-wrap': 'wrap'})
])

# Callback to enable/disable year selection dropdown
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        return True
    return False

# 4.4, 4.5 & 4.6: Callback function to update output charts
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'), Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = df[df['Recession'] == 1]
        
        # Plot 1: Automobile sales fluctuation over Recession Period
        rec_sales = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(rec_sales, x='Year', y='Automobile_Sales', title="Average Automobile Sales Fluctuation Over Recession Period"))
        
        # Plot 2: Average number of vehicles sold by vehicle type
        rec_type = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(rec_type, x='Vehicle_Type', y='Automobile_Sales', title="Average Vehicles Sold by Vehicle Type During Recessions"))
        
        # Plot 3: Total advertisement expenditure share by vehicle type
        rec_ad = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(rec_ad, values='Advertising_Expenditure', names='Vehicle_Type', title="Total Advertising Expenditure Share by Vehicle Type"))
        
        # Plot 4: Effect of unemployment rate on vehicle type and sales
        rec_unemp = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(rec_unemp, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type', title="Effect of Unemployment Rate on Vehicle Type and Sales"))
        
        return [
            html.Div(className='chart-item', children=[R_chart1, R_chart2], style={'width': '50%'}),
            html.Div(className='chart-item', children=[R_chart3, R_chart4], style={'width': '50%'})
        ]

    elif input_year and selected_statistics == 'Yearly Statistics':
        yearly_data = df[df['Year'] == input_year]
        
        # Plot 1: Yearly Automobile Sales
        yas = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales', title="Yearly Automobile Sales"))
        
        # Plot 2: Total Monthly Automobile Sales for selected year
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mas, x='Month', y='Automobile_Sales', title=f"Total Monthly Automobile Sales in {input_year}"))
        
        # Plot 3: Average vehicles sold by vehicle type in selected year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales', title=f"Average Vehicles Sold by Type in {input_year}"))
        
        # Plot 4: Total Advertisement Expenditure for selected year
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type', title=f"Total Advertisement Expenditure by Type in {input_year}"))
        
        return [
            html.Div(className='chart-item', children=[Y_chart1, Y_chart2], style={'width': '50%'}),
            html.Div(className='chart-item', children=[Y_chart3, Y_chart4], style={'width': '50%'})
        ]

    return None

if __name__ == '__main__':
    app.run_server(debug=True)
