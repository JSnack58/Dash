import pandas as pd

class DATASCHEMA:
    AMOUNT = "amount"
    CATEGORY = "category"
    DATE = "date"
    MONTH = "month"
    YEAR = "year"
        

def load_transaction_data(path: str) -> pd.DataFrame:
    # load the data from a CSV file
    data = pd.read_csv(
        path,
        dtype={
            DATASCHEMA.AMOUNT: float,
            DATASCHEMA.CATEGORY: str,
        },
        parse_dates=[DATASCHEMA.DATE]
    )
    data[DATASCHEMA.YEAR] = data[DATASCHEMA.DATE].dt.year.astype(str)
    data[DATASCHEMA.MONTH] = data[DATASCHEMA.DATE].dt.month.astype(str)
    return data