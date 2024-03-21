from dash import Dash, html
from dash_bootstrap_components.themes import BOOTSTRAP
from src.components.layout import create_layout
from src.data.loader import load_transaction_data
from src.data.source import DataSource
import os
import i18n

DATA_PATH = "./Improved_Financial_Dashboard/data/transactions.csv"
LOCALE = "nl"

def main() -> None:
    i18n.set("locale", LOCALE)
    i18n.load_path.append("./Improved_Financial_Dashboard/locale")
    data = load_transaction_data(DATA_PATH,LOCALE)
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = i18n.t("general.app_title")
    app.layout = create_layout(app, DataSource(data))
    app.run()

if __name__ == "__main__":
    main()