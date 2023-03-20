import unittest
from pathlib import Path
import os 
import censusapi.censusgdf as cdf #relative imports
import pandas as pd
import geopandas as gpd


#Test file creation and merging given filepaths
class CreatingFileTest(unittest.TestCase):
    """Blackbox testing for censusgdf.py"""

    #Attributes
    THIS_DIR = Path(__file__).parent
    my_data_path = THIS_DIR /"data"/"input"/ 'testdata.geojson'
    my_output_path = THIS_DIR /"data"/"output"/ 'resultdata.geojson'
    key = os.environ.get('secretUser')
    invalid_path = THIS_DIR /"data"/"test"/"input"/ 'testdata.geojson'

    def test(self):
        self.assertTrue(True)

     #Returns true if the out_pth is created
    def test_out_path(self):
        cdf.add_census_to_geojson(self.my_data_path, self.my_output_path, self.key)
        t = os.path.exists(self.my_output_path)
        self.assertTrue(t)

    #Returns true if the output file is created and it is also a Geopandas dataframe
    def test_filemaking_from_df(self):
        df = gpd.read_file(self.my_data_path)
        out_df = cdf.add_census_to_geojson_df(df,self.key)
        self.assertEqual(type(out_df), type(df))
        
    #Returns true if the output file is created with optional census varaiables
    def test_filemaking_optional_variables_df(self):
        df = gpd.read_file(self.my_data_path)
        variables = ('NAME','B01001_001E')
        out_df = cdf.add_census_to_geojson_df(df,self.key, variables)
        self.assertTrue({'B01001_001E'}.issubset(out_df.columns))


if __name__ == '__main__':
    unittest.main()