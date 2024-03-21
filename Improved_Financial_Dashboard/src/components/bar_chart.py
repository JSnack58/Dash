from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from . import ids
from src.data.loader import DATASCHEMA
import plotly.express as px
import pandas as pd
from ..data.source import DataSource
import i18n


def render(app: Dash, source: DataSource) -> html.Div:
    # Create a callback function that listens in on the year/month-dropdown menus' values.
    @app.callback(
        Output(ids.BAR_CHART, "children"),
        [Input(ids.YEAR_DROPDOWN, "value"), Input(ids.MONTH_DROPDOWN, "value"), Input(ids.CATEGORY_DROPDOWN, "value")]
    )
    # Despite the function not being explicitly called, it is used by the callback above.
    def update_bar_chart(years: list[str], months: list[str], categories: list[str])-> html.Div:
        # Years is the function variable above and is accessible with the '@' prefix
        # in plotly queries(like using {} in f"").
        filtered_source = source.filter(years=years, months=months, categories=categories)
        # Case of no data selected.
        if not filtered_source.row_count:
            return html.Div("No data selected.")
        

        fig = px.bar(
                        data_frame= filtered_source.create_pivot_table(),
                        x=DATASCHEMA.CATEGORY,
                        y=DATASCHEMA.AMOUNT,
                        color=DATASCHEMA.CATEGORY,
                        labels={
                            "category": i18n.t("general.category"),
                            "amount": i18n.t("general.amount")
                                },
                        text=DATASCHEMA.CATEGORY
                    )
        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)
    return html.Div(id=ids.BAR_CHART)