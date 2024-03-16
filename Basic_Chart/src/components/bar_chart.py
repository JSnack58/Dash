from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from . import ids
import plotly.express as px

MEDAL_DATA = px.data.medals_long()

def render(app: Dash) -> html.Div:
    # Create a callback function that listens in on the dropdown menu's values.
    @app.callback(
        Output(ids.BAR_CHART, "children"),
        Input(ids.NATION_DROPDOWN, "value")
    )
    # Despite the function not being explicitly called, it is used by the callback above.
    def update_bar_chart(nations: list[str])-> html.Div:
        # Nations is the function variable above and is accessible with the '@' prefix
        # in plotly queries(like using {} in f"").
        filtered_data = MEDAL_DATA.query("nation in @nations")

        # Case of no data selected.
        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.")

        fig = px.bar(filtered_data, x="medal", y="count", color="nation", text="nation")
        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)
    return html.Div(id=ids.BAR_CHART)