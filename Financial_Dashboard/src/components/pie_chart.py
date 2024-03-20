from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from . import ids
from src.data.loader import DATASCHEMA
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    # Create a callback function that listens in on the year/month-dropdown menus' values.
    @app.callback(
        Output(ids.PIE_CHART, "children"),
        [Input(ids.YEAR_DROPDOWN, "value"), Input(ids.MONTH_DROPDOWN, "value"), Input(ids.CATEGORY_DROPDOWN, "value")]
    )
    # Despite the function not being explicitly called, it is used by the callback above.
    def update_pie_chart(years: list[str], months: list[str], categories: list[str])-> html.Div:
        # Years, months, categories above are accessible with the '@' prefix
        # in plotly queries(like using {} in f"").
        filtered_data = data.query("year in @years and month in @months and category in @categories")

        # Case of no data selected.
        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.", id=ids.PIE_CHART)
        
        pie = go.Pie(
            labels= filtered_data[DATASCHEMA.CATEGORY].tolist(),
            values= filtered_data[DATASCHEMA.AMOUNT].tolist(),
            hole=0.5
        )
        

        fig = go.Figure(data=[pie])
        fig.update_layout(margin={"t":40,"b":0,"l":0,"r":0,})
        fig.update_traces(hovertemplate="%{label}<br>$%{value:.2f}<extra></extra>")
        return html.Div(dcc.Graph(figure=fig), id=ids.PIE_CHART)
    return html.Div(id=ids.PIE_CHART)