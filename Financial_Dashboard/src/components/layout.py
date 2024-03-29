from dash import Dash, html
from . import year_dropdown, month_dropdown, category_dropdown, bar_chart, pie_chart
import pandas as pd
def create_layout(app: Dash, data: pd.DataFrame) -> html.Div:
    return html.Div(
        className = "app-div",
        children = [
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="dropdown-container",
                children=[
                    year_dropdown.render(app, data),
                    month_dropdown.render(app, data),
                    category_dropdown.render(app, data),

                ]
            ),
            bar_chart.render(app, data),
            pie_chart.render(app, data)
        ]
    )