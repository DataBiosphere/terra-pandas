from typing import Optional

import pandas as pd
from terra_notebook_utils import table


def to_dataframe(table_name: str, max_rows: Optional[int]=None) -> pd.DataFrame:
    if max_rows is None:
        ents = [row.attributes for row in table.list_rows(table_name)]
    else:
        ents = [row.attributes for _, row in zip(range(max_rows), table.list_rows(table_name))]
    return pd.DataFrame(ents)

def to_table(table_name: str, df: pd.DataFrame):
    with table.Writer(table_name) as writer:
        for _, series in df.iterrows():
            attributes = dict()
            for name, val in dict(series).items():
                if not pd.isnull(val):
                    key = "-".join(name) if isinstance(name, tuple) else name
                    attributes[key] = val
            writer.put_row(attributes)
