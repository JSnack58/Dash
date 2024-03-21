from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from . import ids
import plotly.graph_objects as go
from ..data.source import DataSource


def render(app: Dash, source: DataSource) -> html.Div:
    # Create a callback function that listens in on the year/month-dropdown menus' values.
    @app.callback(
        Output(ids.PIE_CHART, "children"),
        [Input(ids.YEAR_DROPDOWN, "value"), Input(ids.MONTH_DROPDOWN, "value"), Input(ids.CATEGORY_DROPDOWN, "value")]
    )
    # Despite the function not being explicitly called, it is used by the callback above.
    def update_pie_chart(years: list[str], months: list[str], categories: list[str])-> html.Div:
        # Years, months, categories above are accessible with the '@' prefix
        # in plotly queries(like using {} in f"").
        filtered_source = source.filter(years=years, months=months, categories=categories)

        # Case of no data selected.
        if not filtered_source.row_count:
            return html.Div("No data selected.", id=ids.PIE_CHART)
        
        pie = go.Pie(
            labels= filtered_source.unique_categories,
            values= filtered_source.all_amounts,
            hole=0.5
        )
        

        fig = go.Figure(data=[pie])
        fig.update_layout(margin={"t":40,"b":0,"l":0,"r":0,})
        fig.update_traces(hovertemplate="%{label}<br>$%{value:.2f}<extra></extra>")
        return html.Div(dcc.Graph(figure=fig), id=ids.PIE_CHART)
    return html.Div(id=ids.PIE_CHART)