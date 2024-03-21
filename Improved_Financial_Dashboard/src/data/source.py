from __future__ import annotations
from typing import Optional
from dataclasses import dataclass
# Allows the use of the class name in the class  definition.
import pandas as pd
from .loader import DATASCHEMA

# This class provide abstraction on the frontend component side of the code.
@dataclass
class DataSource:
    _data: pd.DataFrame

    def filter(self, 
               years: Optional[list[str]] = None, 
               months: Optional[list[str]] = None, 
               categories: Optional[list[str]] = None) -> DataSource:
        
        # Make a default for nonexistent arguements.
        if years is None:
            years = self.unique_years
        if months is None:
            months = self.unique_months
        if categories is None:
            categories = self.unique_categories
        # Filter the data via query.
        filtered_data = self._data.query("year in @years and month in @months and category in @categories")
        
        # Create a Datasoruce from the data, and return it.
        return DataSource(filtered_data)
        
    @property
    def all_years(self) -> list[str]:
        return self._data[DATASCHEMA.YEAR].tolist()
    @property
    def unique_years(self) -> list[str]:
        return sorted(set(self._data[DATASCHEMA.YEAR]), key=int)
    @property
    def all_months(self) -> list[str]:
        return self._data[DATASCHEMA.MONTH].tolist()
    @property
    def unique_months(self) -> list[str]:
        return sorted(set(self._data[DATASCHEMA.MONTH]))
    @property
    def all_categories(self) -> list[str]:
        return self._data[DATASCHEMA.CATEGORY].tolist()
    @property
    def unique_categories(self) -> list[str]:
        return sorted(set(self._data[DATASCHEMA.CATEGORY]))
    @property
    def unique_categories(self) -> list[str]:
        return sorted(set(self._data[DATASCHEMA.CATEGORY]))
    @property
    def all_amounts(self) -> list[str]:
        return self._data[DATASCHEMA.AMOUNT].tolist()
    # Convert the category year into amounts.
    # Create a pivot table that sums the amounts of each category.
    def create_pivot_table(self) -> pd.DataFrame:
        pt = self._data.pivot_table(
            values=DATASCHEMA.AMOUNT,
            index=[DATASCHEMA.CATEGORY],
            aggfunc="sum",
            fill_value=0

        )
        return pt.reset_index().sort_values(DATASCHEMA.AMOUNT, ascending=False)
    @property
    def row_count(self) -> int:
        return self._data.shape[0]