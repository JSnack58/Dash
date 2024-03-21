from dash import Dash, html, dcc
from . import ids
from dash.dependencies import Input, Output
from src.data.loader import DATASCHEMA
import pandas as pd
import i18n
from ..data.source import DataSource


def render(app: Dash, source: DataSource) -> html.Div:
    # Callback for when the 'Select All'  button is clicked or the year-dropdown changes
    # to run the following function.
    @app.callback(
        Output(ids.MONTH_DROPDOWN, "value"),
        # The data's record months avaible should depend on the recorded years, so any
        # changes to the years will cause an update to the months.
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_MONTHS_BUTTON, "n_clicks")]
    )
    def update_months(years: list[str], _:int) -> list[str]:
        return source.filter(years=years).unique_months

    return html.Div(
        children = [
            html.H6(i18n.t("general.month")),
            dcc.Dropdown(
                id= ids.MONTH_DROPDOWN,
                options=[{"label":month, "value":month} for month in source.unique_months],
                value = source.unique_months,
                multi=True
            ),
            html.Button(
                className="dropdown-button",
                children=[i18n.t("general.select_all")],
                id=ids.SELECT_ALL_MONTHS_BUTTON,
                n_clicks=0
            )
        ]
    )