import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Load dataset
df = pd.read_csv("insurance.csv")

# Convert categorical variables if needed
df["sex"] = df["sex"].astype("category").cat.codes
df["smoker"] = df["smoker"].astype("category").cat.codes
df["region"] = df["region"].astype("category").cat.codes

# Compute correlation matrix using Spearman method
corr_matrix = df.corr(method="spearman")

# Create a Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Interactive Correlation Heatmap & Scatter Plot"),  # Title

    # Heatmap Graph
    dcc.Graph(id='heatmap'),

    # Scatter Plots
    html.Div([
        dcc.Graph(id='bmi-age-scatter', style={'width': '48%', 'display': 'inline-block'}),
        dcc.Graph(id='bmi-smoke-scatter', style={'width': '48%', 'display': 'inline-block'})
    ]),

    # Histogram
    dcc.Graph(id='bmi-histogram'),

    # Box Plot
    dcc.Graph(id='region-boxplot'),
])

# Callback to update graphs
@app.callback(
    [
        Output('heatmap', 'figure'),
        Output('bmi-age-scatter', 'figure'),
        Output('bmi-smoke-scatter', 'figure'),
        Output('bmi-histogram', 'figure'),
        Output('region-boxplot', 'figure'),
    ],
    Input('heatmap', 'id')  # Dummy input to trigger updates
)
def update_graphs(_):

    # Create heatmap
    heat_fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='Viridis'
    ))
    heat_fig.update_layout(title="Spearman Correlation Heatmap")

    # Scatter plot: BMI vs. Charges (colored by Age)
    bmi_age_fig = px.scatter(df, x="bmi", y="charges", color="age", title="BMI vs. Charges by Age")

    # Scatter plot: BMI vs. Charges (colored by Smoker)
    smoke_fig = px.scatter(df, x="bmi", y="charges", color=df["smoker"].astype(str),
                           title="BMI vs. Charges by Smoking Status")

    # Histogram: BMI vs. Charges (colored by Smoker)
    hist_fig = px.histogram(df, x="bmi", y="charges", color=df["smoker"].astype(str),
                            title="BMI vs. Charges by Smoking Status")

    # Bar plot: Average charges by region
    region_avg = df.groupby("region")["charges"].mean().reset_index()
    boxplot_fig = px.bar(region_avg, x="region", y="charges", color="region",
                         title="Average Insurance Charges by Region")

    return heat_fig, bmi_age_fig, smoke_fig, hist_fig, boxplot_fig


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
