#!/usr/bin/env python
import os
import sys
import time
import unittest

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # noqa
sys.path.insert(0, pkg_root)  # noqa

from tests import config  # initialize the test environment, must preceed terra_notebook_utils import
from terra_pandas import to_dataframe, to_table
from terra_notebook_utils import table


class TestTerraPandas(unittest.TestCase):
    def test_transformation(self):
        start_time = time.time()
        df = to_dataframe("sequencing", 500)
        # df = pd.read_pickle("df.pickle")
        df = df[df['pfb:sample'].notna()]
        df['sample'] = [series['pfb:sample']['entityName'] for _, series in df.iterrows()]
        del df['pfb:sample']
        wide = df.pivot(index="sample",
                        columns="pfb:data_format",
                        values=["pfb:object_id", "pfb:file_size", "pfb:file_name"])
        to_table("sequencing-wide", wide)
        print("Duration", time.time() - start_time)

if __name__ == '__main__':
    unittest.main()
