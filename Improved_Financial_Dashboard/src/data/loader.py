from functools import reduce, partial
from typing import Callable
import babel
import pandas as pd
import datetime as dt
import i18n
from babel.dates import format_date

Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]

def create_year_column(df: pd.DataFrame)-> pd.DataFrame:
    df[DATASCHEMA.YEAR] = df[DATASCHEMA.DATE].dt.year.astype(str)
    return df

def create_month_column(df: pd.DataFrame)-> pd.DataFrame:
    df[DATASCHEMA.MONTH] = df[DATASCHEMA.DATE].dt.month.astype(str)
    return df

def compose(*functions: Preprocessor) -> Preprocessor:
    req = reduce(lambda f,g: lambda x: g(f(x)), functions)
    print("compose return: ",req)
    return req
    # return reduce(lambda f,g: lambda x: g(f(x)), functions)

def translate_date(df: pd.DataFrame, locale: str)-> pd.DataFrame:
    def date_repr(date: dt.date) -> str:
        # Bable is an intergerated translator that can handle the date format per locale.
        return format_date(date, format="MMMM", locale=locale)
    df[DATASCHEMA.MONTH] = df[DATASCHEMA.DATE].apply(date_repr)
    return df

def translate_category(df: pd.DataFrame)-> pd.DataFrame:
    
    def translate(category: dt.date) -> str:
        return i18n.t(f"category.{category}")
    
    df[DATASCHEMA.CATEGORY] = df[DATASCHEMA.CATEGORY].apply(translate)
    return df


class DATASCHEMA:
    AMOUNT = "amount"
    CATEGORY = "category"
    DATE = "date"
    MONTH = "month"
    YEAR = "year"
        

# Translating the data is incrediblely hard while rendering component
# despite it sounding more efficient. The Data must be translated post
# loading.
def load_transaction_data(path: str, locale: str) -> pd.DataFrame:
    # load the data from a CSV file
    data = pd.read_csv(
        path,
        dtype={
            DATASCHEMA.AMOUNT: float,
            DATASCHEMA.CATEGORY: str,
        },
        parse_dates=[DATASCHEMA.DATE]
    )
    preprocessor = compose(create_year_column,
                            create_month_column,
                            # Since translate data takes different arguements unlike other functions
                            # use partial to put in those arguements.
                            partial(translate_date, locale=locale), 
                            translate_category)
    return preprocessor(data)
    