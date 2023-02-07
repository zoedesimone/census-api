import unittest
from pathlib import Path
import os 
import censusapi.censusgdf as cdf #relative imports
import pandas as pd
import geopandas as gpd

class ColumnTest(unittest.TestCase):
    """White box testing for censusgdf.py"""

    #Attributes
    THIS_DIR = Path(__file__).parent
    my_data_path = THIS_DIR /"data"/"input"/ 'testdata.geojson'
    my_output_path = THIS_DIR /"data"/"output"/ 'resultdata.geojson'
    key = os.environ.get('secretUser')
    invalid_path = THIS_DIR /"data"/"test"/"input"/ 'testdata.geojson'

    #Returns true if one of the default columns is written to the new gdf
    def test_default_columns(self):
         df = gpd.read_file(self.my_output_path)
         self.assertTrue({'B19013_001M'}.issubset(df.columns))
    


if __name__ == '__main__':
    unittest.main()