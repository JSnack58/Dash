from dash import Dash, html, dcc
from . import ids
from dash.dependencies import Input, Output
from src.data.loader import DATASCHEMA
import pandas as pd


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_years: list[str] = data[DATASCHEMA.YEAR].tolist()
    unique_years = sorted(set(all_years), key=int)
    # Callback for when the 'Select All' button is clicked to run the following function.
    @app.callback(
        Output(ids.YEAR_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_YEARS_BUTTON, "n_clicks")
    )
    # The function used by the callback above.
    def select_all_years(_: int) -> list[str]:
        return unique_years

    return html.Div(
        children = [
            html.H6("Year"),
            dcc.Dropdown(
                id= ids.YEAR_DROPDOWN,
                options=[{"label":year, "value":year} for year in unique_years],
                value = unique_years,
                multi=True
            ),
            html.Button(
                className="dropdown-button",
                children=["Select All"],
                id=ids.SELECT_ALL_YEARS_BUTTON,
                n_clicks=0
            )
        ]
    )