#!/usr/bin/env python
import os
import sys
import time
import json
import random
import unittest
from uuid import uuid4
from typing import List, Optional

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # noqa
sys.path.insert(0, pkg_root)  # noqa

from tests import config  # initialize the test environment, must preceed terra_notebook_utils import
import terra_pandas as tpd
from terra_notebook_utils import table

class xprofile:
    def __enter__(self, name: str=""):
        self.name = name
        self.start = time.time()
        return self

    def __exit__(self, *kargs, **kwargs):
        print(f"{self.name} duration", time.time() - self.start)

class TestTerraPandas(unittest.TestCase):
    def test_anvil_long_to_wide(self):
        table.delete("sequencing-wide")
        with xprofile():
            tpd.long_to_wide("sequencing", "sequencing-wide", max_rows=500)

    def test_long_to_wide(self):
        table.delete("test-tpd-long")
        table.delete("test-tpd-wide")

        data = dict(a=dict(cram=dict(file_name=f"{uuid4()}", file_size=f"{uuid4()}"),
                           crai=dict(file_name=f"{uuid4()}", file_size=f"{uuid4()}")),
                    b=dict(cram=dict(file_name=f"{uuid4()}", file_size=f"{uuid4()}"),
                           crai=dict(file_name=f"{uuid4()}", file_size=f"{uuid4()}")))

        with table.Writer("test-tpd-long") as writer:
            for ind, obj in data.items():
                for desc, attributes in obj.items():
                    long_row = dict(ind=ind, desc=desc, **attributes)
                    writer.put_row(long_row)

        df = tpd.table_to_dataframe("test-tpd-long")
        tpd.long_to_wide("test-tpd-long",
                         "test-tpd-wide",
                         index_column="ind",
                         header_column="desc",
                         value_columns=["file_name", "file_size"])
        df_wide = tpd.table_to_dataframe("test-tpd-wide")

        for ind, obj in data.items():
            for desc, attributes in obj.items():
                for key, val in attributes.items():
                    self.assertEqual(val, df_wide.loc[ind][f"{key}-{desc}"])

if __name__ == '__main__':
    unittest.main()
