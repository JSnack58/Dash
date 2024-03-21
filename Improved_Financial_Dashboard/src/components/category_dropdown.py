from dash import Dash, html, dcc
from . import ids
from dash.dependencies import Input, Output
import i18n
from ..data.source import DataSource


def render(app: Dash, source: DataSource) -> html.Div:
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
        return source.filter(years=years, months=months).unique_categories
        
    return html.Div(
        children = [
            html.H6(i18n.t("general.category")),
            dcc.Dropdown(
                id= ids.CATEGORY_DROPDOWN,
                options=[{"label":category, "value":category} for category in source.unique_categories],
                value = source.unique_categories,
                multi=True
            ),
            html.Button(
                className="dropdown-button",
                children=[i18n.t("general.select_all")],
                id=ids.SELECT_ALL_CATEGORIES_BUTTON,
                n_clicks=0
            )
        ]
    )