import pandas as pd


class FilterFunction:
    def __init__(self, predicate, col, val):
        """

        Args:
            predicate: str, Predicate, name of a pandas.Series method which returns boolean
            col: str, Name of the column to filter on
            val: dtype of the target column, Value to filter
        """
        self._predicate = getattr(pd.Series, predicate)
        self._col = col
        self._val = val

    def apply(self, df):
        """

        Args:
            df: pd.DataFrame, Data frame to filter

        Returns:
            Filtered DataFrame
        """
        filtered_df = df[self._predicate(df[self._col], self._val)]

        return filtered_df


class Filter:
    def __init__(self, copy=False):
        self._columns = []
        self._predicates = []
        self._values = []
        self._predicate_indexes = []
        self._copy = copy

    def column(self, col):
        self._columns.append(col)

        return self

    def eq(self, value):
        if not self._columns:
            return

        self._predicates.append('eq')
        self._values.append(value)
        self._predicate_indexes.append(len(self._predicates) - 1)

        return self

    def apply(self, df):
        filter_functions = []

        last_index = -1
        for i, predicate in enumerate(self._predicates):
            filter_functions.extend([FilterFunction(predicate, col, self._values[i]) for col in
                                     self._columns[last_index:self._predicate_indexes[i] + 1]])
            last_index = i + 1

        filtered_df = df.copy() if self._copy else df

        for filter_function in filter_functions:
            filtered_df = filter_function.apply(filtered_df)

        return filtered_df
