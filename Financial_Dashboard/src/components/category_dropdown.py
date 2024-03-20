from dash import Dash, html, dcc
from . import ids
from dash.dependencies import Input, Output
from src.data.loader import DATASCHEMA
import pandas as pd


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_categories: list[str] = data[DATASCHEMA.CATEGORY].tolist()
    unique_categories = sorted(set(all_categories))
    # Callback for when the 'Select All'  button is clicked or the year/month-dropdown changes
    # to run the following function.
    @app.callback(
        Output(ids.CATEGORY_DROPDOWN, "value"),
        # The data's recorded categories avaible should depend on the recorded years and months, so any
        # changes to the years or months will cause an update to the categories.
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_CATEGORIES_BUTTON, "n_clicks")]
    )
    def update_categories(years: list[str], months: list[str], _:int) -> list[str]:
        filtered_data = data.query("year in @years and month in @months")
        return sorted(set(filtered_data[DATASCHEMA.CATEGORY].tolist()))

    return html.Div(
        children = [
            html.H6("Category"),
            dcc.Dropdown(
                id= ids.CATEGORY_DROPDOWN,
                options=[{"label":category, "value":category} for category in unique_categories],
                value = unique_categories,
                multi=True
            ),
            html.Button(
                className="dropdown-button",
                children=["Select All"],
                id=ids.SELECT_ALL_CATEGORIES_BUTTON,
                n_clicks=0
            )
        ]
    )