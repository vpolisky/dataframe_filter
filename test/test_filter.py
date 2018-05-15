import pandas as pd

from dataframe_filter.filter import Filter


def test_eq_filter_for_one_column():
    df = pd.DataFrame({'A': [0, 1, 2, 3], 'B': [0, 1, 1, 0]})

    filtered_df = Filter().column('B').eq(1).apply(df)

    assert (
        filtered_df.equals(
            pd.DataFrame({'A': [1, 2], 'B': [1, 1]}, index=[1, 2]))
    )


def test_two_eq_filters_for_distinct_columns():
    df = pd.DataFrame({'A': [0, 1, 2, 3], 'B': [0, 1, 1, 1], 'C': [0, 0, 0, 1]})

    filtered_df = Filter().column('B').eq(1).column('C').eq(1).apply(df)

    assert (
        filtered_df.equals(
            pd.DataFrame({'A': [3], 'B': [1], 'C': [1]}, index=[3]))
    )
