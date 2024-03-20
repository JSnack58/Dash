from dash import Dash, html, dcc
from . import ids
from dash.dependencies import Input, Output
from src.data.loader import DATASCHEMA
import pandas as pd


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_months: list[str] = data[DATASCHEMA.MONTH].tolist()
    unique_months = sorted(set(all_months), key=int)
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
        filtered_data = data.query("year in @years")
        return sorted(set(filtered_data[DATASCHEMA.MONTH].tolist()))

    return html.Div(
        children = [
            html.H6("Month"),
            dcc.Dropdown(
                id= ids.MONTH_DROPDOWN,
                options=[{"label":month, "value":month} for month in unique_months],
                value = unique_months,
                multi=True
            ),
            html.Button(
                className="dropdown-button",
                children=["Select All"],
                id=ids.SELECT_ALL_MONTHS_BUTTON,
                n_clicks=0
            )
        ]
    )