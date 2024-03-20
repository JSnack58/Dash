from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from . import ids
from src.data.loader import DATASCHEMA
import plotly.express as px
import pandas as pd



def render(app: Dash, data: pd.DataFrame) -> html.Div:
    # Create a callback function that listens in on the year/month-dropdown menus' values.
    @app.callback(
        Output(ids.BAR_CHART, "children"),
        [Input(ids.YEAR_DROPDOWN, "value"), Input(ids.MONTH_DROPDOWN, "value"), Input(ids.CATEGORY_DROPDOWN, "value")]
    )
    # Despite the function not being explicitly called, it is used by the callback above.
    def update_bar_chart(years: list[str], months: list[str], categories: list[str])-> html.Div:
        # Years is the function variable above and is accessible with the '@' prefix
        # in plotly queries(like using {} in f"").
        filtered_data = data.query("year in @years and month in @months and category in @categories")

        # Case of no data selected.
        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.")
        
        # Convert the category year into amounts.
        # Create a pivot table that sums the amounts of each category.
        def create_pivot_table() -> pd.DataFrame:
            pt = filtered_data.pivot_table(
                values=DATASCHEMA.AMOUNT,
                index=[DATASCHEMA.CATEGORY],
                aggfunc="sum",
                fill_value=0

            )
            return pt.reset_index().sort_values(DATASCHEMA.AMOUNT, ascending=False)

        fig = px.bar(create_pivot_table(), x=DATASCHEMA.CATEGORY, y=DATASCHEMA.AMOUNT, color=DATASCHEMA.CATEGORY, text=DATASCHEMA.CATEGORY)
        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)
    return html.Div(id=ids.BAR_CHART)