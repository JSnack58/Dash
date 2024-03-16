from dash import Dash, html, dcc
from . import ids
from dash.dependencies import Input, Output

def render(app: Dash) -> html.Div:
    all_nations = ["South Korea", "China", "Canada"]
    # Callback for when the 'Select All' button is clicked to run the following function.
    @app.callback(
        Output(ids.NATION_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_NATIONS_BUTTON, "n_clicks")
    )
    # The function used by the callback above.
    def select_all_nations(_: int) -> list[str]:
        return all_nations

    return html.Div(
        children = [
            html.H6("Nation"),
            dcc.Dropdown(
                id= ids.NATION_DROPDOWN,
                options=[{"label":nation, "value":nation} for nation in all_nations],
                value = all_nations,
                multi=True
            ),
            html.Button(
                className="dropdown-button",
                children=["Select All"],
                id=ids.SELECT_ALL_NATIONS_BUTTON,
            )
        ]
    )