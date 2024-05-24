import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px

# Read the CSV data from the URL
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
df = pd.read_csv(url)

# Data Preparation
# Group data by 'Country/Region' and sum up the values
df_grouped = df.groupby('Country/Region').sum()

# Drop unnecessary columns ('Province/State', 'Lat', 'Long')
df_grouped = df_grouped.drop(columns=['Province/State', 'Lat', 'Long'], errors='ignore')  # data cleaning

# Sort the data by the latest date's total confirmed cases in descending order
df_sorted = df_grouped.sort_values(by=df_grouped.columns[-1], ascending=False)

# Select the top 5 countries with the highest total confirmed cases
top_5_countries = df_sorted.head()

# Create Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("COVID-19 Dashboard"),  # Title of the dashboard
    dcc.Dropdown(
        id='country-dropdown',  # Dropdown for selecting a country
        options=[{'label': country, 'value': country} for country in top_5_countries.index],
        value=top_5_countries.index[0]  # Default value is the first country in the top 5
    ),
    dcc.Graph(id='line-chart'),  # Line chart to show total confirmed cases over time
    dcc.Graph(id='bar-chart'),   # Bar chart to show daily new cases
    dcc.Graph(id='world-map')    # World map to show total confirmed cases by country
])

# Callback to update the line chart based on selected country
@app.callback(
    Output('line-chart', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_line_chart(selected_country):
    # Extract data for the selected country
    data = df_grouped.loc[selected_country]
    x = data.index  # Dates
    y = data.values  # Confirmed cases
    return {
        'data': [go.Scatter(x=x, y=y, mode='lines', name='Confirmed Cases')],
        'layout': go.Layout(title=f"Confirmed COVID-19 Cases in {selected_country}",
                            xaxis={'title': 'Date'},
                            yaxis={'title': 'Confirmed Cases'})
    }

# Callback to update the bar chart based on selected country
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_bar_chart(selected_country):
    # Extract data for the selected country
    data = df_grouped.loc[selected_country]
    daily_new_cases = data.diff().fillna(0)  # Calculate daily new cases
    x = daily_new_cases.index  # Dates
    y = daily_new_cases.values  # Daily new cases
    return {
        'data': [go.Bar(x=x, y=y, name='Daily New Cases')],
        'layout': go.Layout(title=f"Daily New COVID-19 Cases in {selected_country}",
                            xaxis={'title': 'Date'},
                            yaxis={'title': 'Daily New Cases'})
    }

# Callback to update the world map based on selected country
@app.callback(
    Output('world-map', 'figure'),
    [Input('country-dropdown', 'value')]
)
def update_world_map(selected_country):
    # Filter the original data for the selected country
    df_selected = df[df['Country/Region'] == selected_country]
    # Group data by 'Country/Region' and sum up the values
    df_selected_grouped = df_selected.groupby('Country/Region').sum().reset_index()
    # Create a choropleth map
    fig = px.choropleth(df_selected_grouped,
                        locations="Country/Region",
                        locationmode='country names',
                        color=df_selected_grouped.columns[-1],  # Color by the latest date's total cases
                        hover_name="Country/Region",
                        color_continuous_scale="Viridis",
                        title=f"Total Confirmed COVID-19 Cases in {selected_country}")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
